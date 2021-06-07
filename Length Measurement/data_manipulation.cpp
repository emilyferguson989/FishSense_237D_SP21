#include <iostream>
#include <fstream>
#include <math.h>
#include <string>
#include <vector>
#include <stdio.h>
#include <librealsense2/rsutil.h>


//int width, int height, float ppx, float ppy, float fx, float fy, rs2_distortion model, float coeffs[5]

// modified from original function in realsense library
void deproject_pixel_to_point(float point[3], int width, int height, float ppx, float ppy, float fx, float fy, std::string model, float coeffs[5], float pixel[2], float depth)
{
    assert(model != "RS2_DISTORTION_MODIFIED_BROWN_CONRADY"); // Cannot deproject from a forward-distorted image
    //assert(model != "RS2_DISTORTION_BROWN_CONRADY"); // Cannot deproject to an brown conrady model

    float x = (pixel[0] - ppx) / fx;
    float y = (pixel[1] - ppy) / fy;

    float xo = x;
    float yo = y;

    if(model == "RS2_DISTORTION_INVERSE_BROWN_CONRADY")
    {
        // need to loop until convergence 
        // 10 iterations determined empirically
        for (int i = 0; i < 10; i++)
        {
            float r2 = x * x + y * y;
            float icdist = (float)1 / (float)(1 + ((coeffs[4] * r2 + coeffs[1])*r2 + coeffs[0])*r2);
            float xq = x / icdist;
            float yq = y / icdist;
            float delta_x = 2 * coeffs[2] * xq*yq + coeffs[3] * (r2 + 2 * xq*xq);
            float delta_y = 2 * coeffs[3] * xq*yq + coeffs[2] * (r2 + 2 * yq*yq);
            x = (xo - delta_x)*icdist;
            y = (yo - delta_y)*icdist;
        }
    }
    if (model == "RS2_DISTORTION_BROWN_CONRADY")
    {
        // need to loop until convergence 
        // 10 iterations determined empirically
        for (int i = 0; i < 10; i++)
        {
            float r2 = x * x + y * y;
            float icdist = (float)1 / (float)(1 + ((coeffs[4] * r2 + coeffs[1])*r2 + coeffs[0])*r2);
            float delta_x = 2 * coeffs[2] * x*y + coeffs[3] * (r2 + 2 * x*x);
            float delta_y = 2 * coeffs[3] * x*y + coeffs[2] * (r2 + 2 * y*y);
            x = (xo - delta_x)*icdist;
            y = (yo - delta_y)*icdist;
        }
        
    }
    if (model == "RS2_DISTORTION_KANNALA_BRANDT4")
    {
        float rd = sqrtf(x*x + y*y);
        if (rd < FLT_EPSILON)
        {
            rd = FLT_EPSILON;
        }

        float theta = rd;
        float theta2 = rd*rd;
        for (int i = 0; i < 4; i++)
        {
            float f = theta*(1 + theta2*(coeffs[0] + theta2*(coeffs[1] + theta2*(coeffs[2] + theta2*coeffs[3])))) - rd;
            if (fabs(f) < FLT_EPSILON)
            {
                break;
            }
            float df = 1 + theta2*(3 * coeffs[0] + theta2*(5 * coeffs[1] + theta2*(7 * coeffs[2] + 9 * theta2*coeffs[3])));
            theta -= f / df;
            theta2 = theta*theta;
        }
        float r = tan(theta);
        x *= r / rd;
        y *= r / rd;
    }
    if (model == "RS2_DISTORTION_FTHETA")
    {
        float rd = sqrtf(x*x + y*y);
        if (rd < FLT_EPSILON)
        {
            rd = FLT_EPSILON;
        }
        float r = (float)(tan(coeffs[0] * rd) / atan(2 * tan(coeffs[0] / 2.0f)));
        x *= r / rd;
        y *= r / rd;
    }

    point[0] = depth * x;
    point[1] = depth * y;
    point[2] = depth;
}

// helper function
std::vector<std::string> split_string(std::string text) {
    std::vector<std::string> result;

    // split the index before ":":
    if (text[1] == ':') {
        result.push_back(text.substr(0, 1));
        text.erase(text.begin(), text.begin()+2);
    }
    else if (text[2] == ':') {
        result.push_back(text.substr(0, 2));
        text.erase(text.begin(), text.begin()+3);
    }
    else if (text[3] == ':') {
        result.push_back(text.substr(0, 3));
        text.erase(text.begin(), text.begin()+4);
    }

    // split each coordinate
    std::string delimeter = ",";
    std::string sub_str = "";
    int pos = 0;
    while ((pos = text.find(delimeter)) != (int)std::string::npos) {
        sub_str = text.substr(0, pos);
	result.push_back(sub_str);
	text.erase(text.begin(), text.begin()+pos+1);
    }
    result.push_back(text);

    return result;
}

int main() {
    remove("length_full.txt");
    remove("length_only.txt");
  
    int i_index = 0;
    int j_index = 0;
    float points[106*2][3] = {0};

    // read in indecies and coordinates in mean vector
    std::string line;
    std::ifstream pts_vec ("./mean_points.txt");
    if (pts_vec.is_open()) {
        while (getline(pts_vec, line)) {
	    std::vector<std::string> pts = split_string(line);
	    int index = stoi(pts[0]);
	    points[index*2][0] = stof(pts[1]);
	    points[index*2][1] = stof(pts[2]);
	    points[index*2][2] = stof(pts[3]);
	    points[index*2+1][0] = stof(pts[4]);
	    points[index*2+1][1] = stof(pts[5]);
	    points[index*2+1][2] = stof(pts[6]);
	}
    }
      
    int width;
    int height;
    float ppx;
    float ppy;
    float fx;
    float fy;
    std::string model;
    float coeffs[5];
    std::vector<std::string> matrix;

    // read in parameters in intrinsic matrix
    std::ifstream matrix_data ("./intrinsic_matrix.txt");
    if (matrix_data.is_open()) {
        while (getline(matrix_data, line)) {
	    matrix.push_back(line);
	}
    }

    width = stoi(matrix[0]);
    height = stoi(matrix[1]);
    ppx = stof(matrix[2]);
    ppy = stof(matrix[3]);
    fx = stof(matrix[4]);
    fy = stof(matrix[5]);
    model = matrix[6];
    for (int i = 0; i < 5; i++) {
        coeffs[i] = stof(matrix[7+i]);
    }
    

    // transfer from color 2d pixel to color 3d space
    float point1[3];
    float point2[3];
    float pixel1[2];
    float pixel2[2];
    float depth1;
    float depth2;
  
    for (int i = 0; i < 106; i++) {
        // skip those without assigning x,y,depth info
        if (points[i*2][2] == 0) {
	  continue;
        }
	
        pixel1[0] = points[i*2][0];
	pixel1[1] = points[i*2][1];
	depth1 = points[i*2][2];
	pixel2[0] = points[i*2+1][0];
	pixel2[1] = points[i*2+1][1];
	depth2 = points[i*2+1][2];
	
        deproject_pixel_to_point(point1, width, height, ppx, ppy, fx, fy, model, coeffs, pixel1, depth1);
	deproject_pixel_to_point(point2, width, height, ppx, ppy, fx, fy, model, coeffs, pixel2, depth2);
    
	//std::cout << "head: " <<  point1[0] << " " << point1[1] << " " << point1[2] << std::endl;
	//std::cout << "tail: " << point2[0] << " " << point2[1] << " " << point2[2] << std::endl;
	float dis = sqrt(pow(point1[0]-point2[0], 2) + pow(point1[1]-point2[1], 2) + pow(point1[2]-point2[2], 2));
	//std::cout << "distance/fish length: " << dis << std::endl;
	//std::cout << std::endl;

	std::ofstream length_full("length_full.txt", std::ios::app);
	length_full << "image " << i << ":" << std::endl;
	length_full << "head: " << point1[0] << " " << point1[1] << " " << point1[2] << std::endl;
	length_full << "tail: " << point2[0] << " " << point2[1] << " " << point2[2] << std::endl;
	length_full << "distance/fish length: " << dis << std::endl;
	length_full << std::endl;

	std::ofstream length_only("length_only.txt", std::ios::app);
	length_only << i << ":" << dis << std::endl;
    }
    
      
    return 0;
 }


// read in csv file
// save as Mat/vector of vector
// points needed are read from color image

// read in intrinsic matrix line by line in string 
// and then change it back to the original type
// i.e., int, float

// transform from color 2D pixel frame to color 3D camera frame
// remember depth here is from the Mat result (mapped depth image)
//            rs2_deproject_pixel_to_point

// transform from depth 3D camera frame to world 3D frame
// as the origin of color camera frame is the same as that of world frame
// Rotation is just [1,0,0; 0,1,0;0,0,1], Translation is [0;0;0]
// so the 3d coordinates in color frame is just the world coordinates
