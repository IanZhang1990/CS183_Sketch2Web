/**
 * Simple shape detector program.
 * It loads an image and tries to find simple shapes (rectangle, triangle, circle, etc) in it.
 * This program is a modified version of `squares.cpp` found in the OpenCV sample dir.
 */
#include <vector>

#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cmath>
#include <iostream>

void sharpen(cv::Mat &image, cv::Mat &result)  
{  
	result.create(image.size(),image.type());  
	//the first ,last row and colum do not process , bucause they do not have up or left neighbour  
	for(int i = 1; i<image.rows-1; i++)  
	{  
		const uchar* previous = image.ptr<const uchar>(i-1);  
		const uchar* current = image.ptr<const uchar>(i);  
		const uchar* next = image.ptr<const uchar>(i+1);  

		uchar* output = result.ptr<uchar>(i);  

		for (int j=1; j<image.cols-1 ;j++ )  
			*output++ = cv::saturate_cast<uchar>(5*current[j]-current[j-1]-current[j+1]-previous[j]-next[j]);  
	}  
	//Set the unprocess pixels to 0  
	result.row(0).setTo(cv::Scalar(0));  
	result.row(result.rows-1).setTo(cv::Scalar(0));  
	result.col(0).setTo(cv::Scalar(0));  
	result.col(result.cols-1).setTo(cv::Scalar(0));  
}  

/**
 * Helper function to find a cosine of angle between vectors
 * from pt0->pt1 and pt0->pt2
 */
static double angle(cv::Point pt1, cv::Point pt2, cv::Point pt0)
{
	double dx1 = pt1.x - pt0.x;
	double dy1 = pt1.y - pt0.y;
	double dx2 = pt2.x - pt0.x;
	double dy2 = pt2.y - pt0.y;
	return (dx1*dx2 + dy1*dy2)/sqrt((dx1*dx1 + dy1*dy1)*(dx2*dx2 + dy2*dy2) + 1e-10);
}

/**
 * Helper function to display text in the center of a contour
 */
void setLabel(cv::Mat& im, const std::string label, std::vector<cv::Point>& contour)
{
	int fontface = cv::FONT_HERSHEY_SIMPLEX;
	double scale = 0.4;
	int thickness = 1;
	int baseline = 0;

	cv::Size text = cv::getTextSize(label, fontface, scale, thickness, &baseline);
	cv::Rect r = cv::boundingRect(contour);

	cv::Point pt(r.x + ((r.width - text.width) / 2), r.y + ((r.height + text.height) / 2));
	cv::rectangle(im, pt + cv::Point(0, baseline), pt + cv::Point(text.width, -text.height), CV_RGB(255,255,255), CV_FILLED);
	cv::putText(im, label, pt, fontface, scale, CV_RGB(0,0,0), thickness, 8);
}

int main()
{
	//cv::Mat src = cv::imread("polygon.png");
	//cv::Mat src = cv::imread("C:/Users/ianzh_000/Documents/GitHub/CS183_Sketch2Web/Source/Debug/basic-shapes2.png");
	cv::Mat src = cv::imread("C:/Users/ianzh_000/Documents/GitHub/CS183_Sketch2Web/Source/Debug/outputImg.jpg");

	if (src.empty())
		return -1;

	// Convert to grayscale
	cv::Mat gray;
	cv::cvtColor(src, gray, CV_BGR2GRAY);

	// Sharpen the image
	//cv::Mat sharp;
	//sharpen( gray, sharp );
	//cv::imshow("Sharpen", sharp);

	// Blur the image
	//cv::Mat blurred;
	//cv::blur( gray, blurred, cv::Size( 3, 3 ) );
	//cv::imshow("Blur", blurred);

	// Convert to black and white image
	cv::Mat bw;
	cv::threshold(gray, bw, 140, 255.0, cv::THRESH_BINARY);

	// Use Canny instead of threshold to catch squares with gradient shading
	cv::Mat canny;
	cv::Canny(bw, canny, 0, 50, 5);
	cv::imshow("Canny", canny);

	// Find contours
	std::vector<std::vector<cv::Point> > contours;
	cv::findContours(canny.clone(), contours, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE);

	std::vector<cv::Point> approx;
	cv::Mat dst = src.clone();

	cv::RNG rng(12345);
	std::vector<cv::Rect> boundRect( contours.size() );
	std::vector<cv::Point2f>center( contours.size() );
	std::vector<float>radius( contours.size() );


	for (int i = 0; i < contours.size(); i++)
	{
		// Approximate contour with accuracy proportional
		// to the contour perimeter
		cv::approxPolyDP(cv::Mat(contours[i]), approx, cv::arcLength(cv::Mat(contours[i]), true)*0.02, true);

		// Skip small or non-convex objects 
		if (std::fabs(cv::contourArea(contours[i])) < 100 || !cv::isContourConvex(approx))
			continue;

		if (approx.size() == 3)
		{
			setLabel(dst, "TRI", contours[i]);    // Triangles
		}
		else if (approx.size() >= 4 && approx.size() <= 6)
		{
			// Number of vertices of polygonal curve
			int vtc = approx.size();

			// Get the cosines of all corners
			std::vector<double> cos;
			for (int j = 2; j < vtc+1; j++)
				cos.push_back(angle(approx[j%vtc], approx[j-2], approx[j-1]));

			// Sort ascending the cosine values
			std::sort(cos.begin(), cos.end());

			// Get the lowest and the highest cosine
			double mincos = cos.front();
			double maxcos = cos.back();

			// Use the degrees obtained above and the number of vertices
			// to determine the shape of the contour
			if (vtc == 4 && mincos >= -0.1 && maxcos <= 0.3)
			{
				setLabel(dst, "RECT", contours[i]);
			}
			else if (vtc == 5 && mincos >= -0.34 && maxcos <= -0.27)
			{
				setLabel(dst, "PENTA", contours[i]);
			}
			//else if (vtc == 6 && mincos >= -0.55 && maxcos <= -0.45)
			//	setLabel(dst, "HEXA", contours[i]);

		}
		else
		{
			// Detect and label circles
			double area = cv::contourArea(contours[i]);
			cv::Rect r = cv::boundingRect(contours[i]);
			int radius = r.width / 2;

			if (std::abs(1 - ((double)r.width / r.height)) <= 0.2 &&
			    std::abs(1 - (area / (CV_PI * std::pow((double)(radius), 2)))) <= 0.2)
				setLabel(dst, "CIR", contours[i]);
		}

		boundRect[i] = cv::boundingRect( contours[i] );
		//cv::minEnclosingCircle( contours[i], center[i], radius[i] );
	}

	for( int i = 0; i< contours.size(); i++ )
	{
		cv::Scalar color = cv::Scalar( rng.uniform(0, 255), rng.uniform(0,255), rng.uniform(0,255) );
		drawContours( src, contours, i, color, 1, 8, std::vector<cv::Vec4i>(), 0, cv::Point() );
		rectangle( src, boundRect[i].tl(), boundRect[i].br(), color, 2, 8, 0 );
		//circle( src, center[i], (int)radius[i], color, 2, 8, 0 );
	}


	cv::imshow("src", src);
	cv::imshow("dst", dst);
	cv::waitKey(0);
	return 0;
}