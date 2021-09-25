package GUI;
import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Desktop;
import java.awt.Image;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.Scanner;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JPanel;

public class Main {
 
	public static void main(String[] args) {
		
		
		//创建窗口
        JFrame f = new JFrame("ImageMatting");
        //容器放进窗口
        Container contentPane = new Container();
        f.setContentPane(contentPane);
        //设置容器布局
        contentPane.setLayout(new BorderLayout());//边界布局
        
        JPanel p1 = new JPanel();
        //PS: 设置面板背景色为蓝色，如果不引入AWT包，程序将出错，可以试试看
        p1.setBackground(Color.GRAY);
        p1.setSize(200,800);           //设置面板对象大小
        
        JButton b1 = new JButton("查看所有图片");
        b1.setBounds(25,10,150,50);
        JButton b2 = new JButton("Start！");
        b2.setBounds(25,500,150,50);
        //JLabel l = new JLabel("请输入想要处理的图片：");
		p1.add(b1);
        p1.add(b2);
        //p1.add(l);
        
        contentPane.add(p1, BorderLayout.WEST);
        
        
        
        JPanel p2 = new JPanel();
        contentPane.add(p2, BorderLayout.EAST);
        
        
        //设置图片路径变量
        String str = "C:\\Users\\pc\\Desktop\\image_matting-main\\image_matting-main\\data";//用来打开所有图片文件夹
        
        
        
        //b1鼠标点击事件
	    b1.addMouseListener( new MouseAdapter() {
	    	public void mouseClicked(MouseEvent e) {//鼠标点击事件
	    		
	    		try {
	                File file = new File(str); // 创建文件对象
	                Desktop.getDesktop().open(file); // 启动已在本机桌面上注册的关联应用程序，打开文件文件file。
	            } catch (IOException | NullPointerException e1) { // 异常处理
	                System.err.println(e1);
	            }
	    	}//鼠标点击事件结束
	    });//按钮监听结束
	    
	    
	    
		
	    
	    //b2鼠标点击事件
	    b2.addMouseListener( new MouseAdapter() {
	    	public void mouseClicked(MouseEvent e) {//鼠标点击事件
	    		
	    		//接收python给的图地址
	    		try {
	    			
	    			
	    			//输入
	    			Scanner myscanner = new Scanner(System.in);
	    			String a;//传给python的变量——图片名
	    			System.out.println("请输入图片名：");
	    			a = myscanner.next();
	    			
	    			p2.removeAll();//清除面板2中内容
	    			
	    			//执行python
	    			String[] args1 = new String[] { "python", "D:\\codespython\\test.py", a };//传参数
	    			//String[] args1 = new String[] { "python", "C:\\Users\\pc\\Desktop\\image_matting-main (1)\\image_matting-main\\main.py", a };//传参数
	    			Process proc = Runtime.getRuntime().exec(args1);// 准备进程 —— 执行py文件
	    			BufferedReader in = new BufferedReader(new InputStreamReader(proc.getInputStream()));//进程
	    			String line = null;
	    			line = in.readLine();
	    		    System.out.println(line);//line是返回的地址
	    		
	    			//准备图片
		    		int width = 775;
		    		int height = 755;
		    		//创建图片
		    		ImageIcon image = new ImageIcon(line);
		            //创建面板
		            image.setImage(image.getImage().getScaledInstance(width,height,Image.SCALE_DEFAULT));
		            //创建标签，并加入图片
		            JLabel label = new JLabel(image, JLabel.CENTER);
		            //面板加入标签
		            
		            p2.add(label);
		    		
		    		//刷新
		    		f.setVisible(false);
		    		f.setVisible(true);
	    			
	    			in.close();//关闭BufferedReader
	    			proc.waitFor();//进程proc等待
	    		} catch (IOException e1) {
	    			e1.printStackTrace();
	    		} catch (InterruptedException e2) {
	    			e2.printStackTrace();
	    		}
	    		
	    		
	    		
	    		
	    	}//鼠标点击事件结束
	    });
	    
	    
        //写在最后
        //设置号窗口位置
        f.setLocation(400,100);
        //设置窗口大小
        f.setSize(1000,800);
        //不能改变大小
        f.setResizable(false);
        //显示窗口
        f.setVisible(true);
    }
}

