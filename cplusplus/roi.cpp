/*
  a simple program demonstrating the use of Tesseract OCR engine with OpenCV,
  adopted from http://www.sk-spell.sk.cx/simple-example-how-to-call-use-tesseract-library
 */

#include <baseapi.h>
#include <map>
#include <sys/time.h>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>

#include <tesseract/baseapi.h>
#include <leptonica/allheaders.h>

#include <iostream>

#include <cctype>
#include <fstream>


using namespace cv;
using namespace std;



string DataOCR(Mat image){

  string outText;
  Mat im = image.clone();
  resize(im, im, cv::Size(), 0.7, 0.7);

  tesseract::TessBaseAPI *ocr = new tesseract::TessBaseAPI();
  ocr->Init(NULL, "por", tesseract::OEM_TESSERACT_ONLY);
  ocr->SetPageSegMode(tesseract::PSM_SINGLE_LINE);
  ocr->SetVariable("tessedit_char_whitelist","0123456789.");
  // ocr->SetVariable("preserve_interword_spaces","0");
  ocr->SetVariable("options", "digits");


  ocr->SetImage(im.data, im.cols, im.rows, im.channels(), im.step);
  outText = string(ocr->GetUTF8Text());

  ocr->End();


  outText.erase(std::remove_if(outText.begin(), outText.end(), ::isspace), outText.end());

  for (int i = 0; i < outText.size(); i++){
    if (outText[i] == '.')
      outText[i] = '/';
  }

  cout << "\n\n-> Resultado: ";
  cout << outText;
  cout << "\n";

  // imshow("imagem", im);
  // waitKey(0);


  return outText;


}




int main(int argc, char* argv[]) {

  string im_path = argv[1];


  // map<string, string> Covid_Data;


  Mat LoadedImage, OutImage;
  LoadedImage = imread(im_path, IMREAD_COLOR);

  OutImage = LoadedImage.clone();
  // inRange(OutImage, 101, 255, OutImage);
  // threshold(OutImage, OutImage, 100, 255, THRESH_BINARY);

  Size size(1134,1134);

  resize(LoadedImage,LoadedImage,size);//resize image

  cvtColor( LoadedImage, OutImage, COLOR_BGR2GRAY );



  Mat Mask;
  inRange(OutImage,0,100,Mask);
  OutImage.setTo(0,Mask);


  Mat Mask2;
  inRange(OutImage,100,255,Mask2);
  OutImage.setTo(255,Mask2);


  // namedWindow("Boletim COVID-19", WINDOW_AUTOSIZE);


   // imshow("Boletim COVID-19", LoadedImage);
   //  waitKey(0);


// This construct Rectangle Rec start at x=100 y=100, width=200 and heigth=200


  // PACIENTES COM SRAG

  // -- NOTIFICADOS

  Rect Not_Total(45, 571, 510, 133);


  Rect Not_Susp(45, 720, 168, 95);
  Rect Not_Desc(219, 720, 168, 95);
  Rect Not_Conf(392, 720, 168, 95);


  // -- INTERNADOS


  Rect Int_Susp(576, 571, 171, 75);
  Rect Int_Conf(748, 571, 171, 75);
  Rect Int_Tot(918, 571, 171, 75);



  // -- ÓBITOS


  Rect Obt_Susp(576, 741, 171, 75);
  Rect Obt_Conf(748, 741, 171, 75);
  Rect Obt_Tot(918, 741, 171, 75);


  // -- Data

  Rect Data(588, 386, 140, 40);



  // -- CASOS LEVES


  Rect Lev_Tot(661, 1008, 260, 80);

  // Rect Recs[10];



 // Desenhar retangulos


  // rectangle(OutImage, Not_Total, Scalar(255), 1, 8, 0);
  // rectangle(OutImage, Not_Susp, Scalar(255), 1, 8, 0);
  // rectangle(OutImage, Not_Desc, Scalar(255), 1, 8, 0);
  // rectangle(OutImage, Not_Conf, Scalar(255), 1, 8, 0);

  // rectangle(OutImage, Int_Susp, Scalar(255), 1, 8, 0);
  // rectangle(OutImage, Int_Conf, Scalar(255), 1, 8, 0);
  // rectangle(OutImage, Int_Tot, Scalar(255), 1, 8, 0);

  //   rectangle(OutImage, Obt_Susp, Scalar(255), 1, 8, 0);
  // rectangle(OutImage, Obt_Conf, Scalar(255), 1, 8, 0);
  // rectangle(OutImage, Obt_Tot, Scalar(255), 1, 8, 0);

  // rectangle(OutImage, Data, Scalar(255), 1, 8, 0);

  // rectangle(OutImage, Lev_Tot, Scalar(255), 1, 8, 0);



 // REGION OF INTEREST


  // -- NOTIFICADOS

  Mat Roi_Not_Total = OutImage(Not_Total);
  Mat Roi_Not_Susp = OutImage(Not_Susp);
  Mat Roi_Not_Desc = OutImage(Not_Desc);
  Mat Roi_Not_Conf = OutImage(Not_Conf);


  // -- INTERNADOS

  Mat Roi_Int_Susp = OutImage(Int_Susp);
  Mat Roi_Int_Conf = OutImage(Int_Conf);
  Mat Roi_Int_Tot = OutImage(Int_Tot);


  // -- ÓBITOS


   Mat Roi_Obt_Susp = OutImage(Obt_Susp);
   Mat Roi_Obt_Conf = OutImage(Obt_Conf);
   Mat Roi_Obt_Tot = OutImage(Obt_Tot);


  // -- Data
  
  Mat Roi_Data = OutImage(Data);



  // -- CASOS LEVES


  Mat Roi_Lev_Tot = OutImage(Lev_Tot);


// INFORMAÇÕES






  // Covid_Data["SRAG Notificados"] = 10;


  ofstream file;
  file.open("dados.csv", ios_base::app);

  file << DataOCR(Roi_Data);
  file << ";";



  file << DataOCR(Roi_Not_Total);
  file << ";";

  file << DataOCR(Roi_Not_Susp);
  file << ";";

  file << DataOCR(Roi_Not_Desc);
  file << ";";

  file << DataOCR(Roi_Not_Conf);
  file << ";";



  // -- INTERNADOS

  file << DataOCR(Roi_Int_Susp);
  file << ";";

  file << DataOCR(Roi_Int_Conf);
  file << ";";

  file << DataOCR(Roi_Int_Tot);
  file << ";";


  // -- ÓBITOS


   file << DataOCR(Roi_Obt_Susp);
   file << ";";

   file << DataOCR(Roi_Obt_Conf);
   file << ";";

   file << DataOCR(Roi_Obt_Tot);
   file << ";";


  // -- CASOS LEVES


  file << DataOCR(Roi_Lev_Tot);


  file << "\n";
  file.close();






  return 0;
}