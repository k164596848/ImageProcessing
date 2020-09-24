using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using Emgu.CV.CvEnum;
using Emgu.CV;
using Emgu.CV.Structure;
using Emgu.Util;


namespace ImageProcessing
{
    public partial class Form1 : Form
    {      


        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void button_loadimage_Click(object sender, EventArgs e)
        {
            imageBox1.Image = null;
            imageBox2.Image = null;
            imageBox3.Image = null;
            imageBox4.Image = null;
            //開啟檔案
            OpenFileDialog filename = new OpenFileDialog();
            if (filename.ShowDialog() == DialogResult.OK)
            {
                //將檔案路經存至Textbox1
                textBox1.Text = filename.FileName;

                
            }
        }

        private void textBox1_TextChange(object seder,EventArgs e)
        {
            //將影像變形至400*400

            //讀取彩色影像
            Image<Bgr, byte> colorImage = new Image<Bgr, byte>(textBox1.Text);
            imageBox1.Image = colorImage;

            //取得灰階影像
            Image<Gray, byte> grayImage = colorImage.Convert<Gray, byte>();
            grayImage.Save(textBox1.Text+"gray.jpg" );
            imageBox2.Image = grayImage;

             
            //二值化的閥值
            Gray thresholdValue = new Gray(140);
            //取得二值化影像
            Image<Gray, byte> thresholdImage = grayImage.ThresholdBinary(thresholdValue, new Gray(255));          
            //灰度反轉
            //thresholdImage = 255 - thresholdImage;            
            imageBox3.Image = thresholdImage;
            thresholdImage.Save(textBox1.Text + "threshold.jpg");


            //擴張處理(擴張x像素)
            Image<Gray, byte> ErodeImage = thresholdImage.Erode(1);
            imageBox4.Image = ErodeImage;
            ErodeImage.Save(textBox1.Text + "Ecode.jpg");




        }

    }
}
