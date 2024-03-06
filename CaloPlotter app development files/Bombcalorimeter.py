# -*- coding: utf-8 -*-

from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import serial
import time
import numpy as np
from scipy.interpolate import interp1d
import sys
from PIL import Image, ImageDraw, ImageFont, ImageTk, ImageChops
import os
import base64
import os
import sys

os.chdir(os.path.dirname(__file__))
image_path=os.path.join(sys._MEIPASS, "bomb.jpg")


image_opacity = 255
text_opacity = 0

def fade_image_and_text():
    global image_opacity, text_opacity, text_image,image_label

    if image_opacity >= 0:
        # Open the image
        image = Image.open(image_path)
        image = image.resize((1000, 1000))
        if image.mode != "RGBA":
            image = image.convert("RGBA")
        # Create text image
        text_image = Image.new("RGBA", (1000, 1000), (255, 255, 255, text_opacity))  # Transparent background
        draw = ImageDraw.Draw(text_image)
        font = ImageFont.truetype("arial.ttf", 80)
        font1 = ImageFont.truetype("arial.ttf", 36)
        text = "CaloPlotter"
        texto="Acknowledgment\nDr. Kazi Arafat Rahman, Assistant Professor\nPriom Das, Lecturer\nShahriar Alam, Lecturer\nSakib Javed, Lecturer"
        draw.text((300, 400), text, fill=(100, 30, 20, text_opacity), font=font)  # Draw text with full opacity
        draw.text((20, 650), texto, fill=(100, 30, 20, text_opacity), font=font1)

        # Calculate blended image opacity
        blended_opacity = min(255, text_opacity)  # Ensure smooth transition

        # Create an opaque mask image
        mask_image = Image.new("L", (1000, 1000), 255)  # White mask (fully opaque)
        mask_image = mask_image.convert("RGBA")
        # Apply image opacity to the mask
        mask_image.putalpha(image_opacity)

        # Create a transparent image for blending
        transparent_image = Image.new("RGBA", (1000, 1000), (255, 255, 255, image_opacity))

        # Combine mask and transparent image with blended opacity
        transparent_image = ImageChops.multiply(mask_image, transparent_image)
        transparent_image.putalpha(blended_opacity)

        blended_image = Image.alpha_composite(image, text_image)

        # Apply transparent image with blended opacity
        blended_image = ImageChops.multiply(blended_image, transparent_image)

        # Update image label
        photo = ImageTk.PhotoImage(blended_image)
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference

        # Update opacities for next iteration
        image_opacity -= 8
        text_opacity += 8

        root.after(100, fade_image_and_text)  # Repeat after a short delay
    else:
        # After fade completes, show the wel_fr frame
        time.sleep(3)  # Optional delay
        image_label.destroy()
        wel_fr.pack(expand=True, fill="both")
        welcome_label.pack(pady=60)
        text_labelin.pack(anchor='nw' )
        #labelac.pack(side=LEFT,anchor='sw',padx=10,pady=10)  # Pack at the bottom right corner
        labelid.pack(side=RIGHT,anchor='se',padx=10,pady=10)  # Pack at the bottom right corner
        proceed_button.pack(pady=50)
        # ... (rest of your code for wel_fr)


        #root.after(1000, root.destroy)  # Destroy window after image and text fade out


dataList = []
yList = []

num1 = 1e9
num2 = 1e9
num3 = 1e9
num4 = 1e9
num5 = 1e9
num6 = 1e9
num7 = 1e9
num8=1e9
num9=1e9
num10 = 0
fo=0
x=0
ok=0


# Create the main window
root = Tk()



#root.protocol("WM_DELETE_WINDOW", root.destroy())
root.state('zoomed')






def appo():
    wel_fr.destroy()
    ser = serial.Serial("COM4", 9600)
    fig, ax = plt.subplots(facecolor='#D3D3D3')  # Create figure and subplot
     # Create the plot canvas
    plt.gca().set_facecolor('black')
    
    time.sleep(2)
   
     
    #define the animate function to trigger the frames periodically
    def animate(i):
        global fo
        global start_time
        global dataList
        global yList
        global ok
        
        
        ser.write(b'g')
        arduinoData_string = ser.readline()
        
        try:
            arduinoData_float = float(arduinoData_string)
            dataList.append(arduinoData_float)
            yList.append(float(i/60))
            
        except:
            pass
        if i>300 and ok==0 : # and dataList[i-1]-dataList[i] < 1e-3:
            ok=1
            ax.clear()
            ax.plot(yList, dataList,color='#ff0490', linewidth=2)
            ax.set_ylim([20,30])
            ax.set_title("Arduino Data",fontsize=20,fontdict={'color': '#3B444B'},pad=10)
            ax.set_ylabel("Temperature (Degree Celsius)",fontsize=16,fontdict={'color': '#3B444B'},labelpad=10)
            ax.set_xlabel("Time (Minute)",fontsize=16,fontdict={'color': '#3B444B'},labelpad=10)
            root.after(900000, ani.event_source.stop)#timer to close the serial and plotting after 5 minutes of tc
            root.after(900000,after_animation_stops)           
        else:   
            ax.clear()
            ax.plot(yList, dataList,color='#ff0490', linewidth=2)
            ax.set_ylim([20,30])
            ax.set_title("Arduino Data",fontsize=16,fontdict={'color': '#3B444B'},pad=10)
            ax.set_ylabel("Temperature (Degree Celsius)",fontsize=16,fontdict={'color': '#3B444B'},labelpad=10)
            ax.set_xlabel("Time (Minute)",fontsize=16,fontdict={'color': '#3B444B'},labelpad=10)

    def after_animation_stops():
        global fo
        global dataList
        global yList
        global max_value
        global num1;
        global num2;
        global num3;
        global num4;
        global num5;
        global num6;
        global num7;
        global num10;
        sliced_data1 = dataList[300:600 + 1]
        st_ind=int(300)
        #max_value= float(max(sliced_data1))        
        ind=sliced_data1.index(max(sliced_data1))
        fo=st_ind+ind
        
        num1 = float(max(sliced_data1))
        num2 = float(dataList[300])
        num3 = float((dataList[300]-dataList[0])/5)
        num4 = float((dataList[fo+300]-dataList[fo])/5)
        num5 = float(5)
            
        num7 = float(fo/60)
        
        num10 = float(2420)
        
        start_index=int(300)
        target_number=float(dataList[300]+0.6*(dataList[fo]-dataList[300]))
        sliced_data = dataList[300:fo + 1]

        # Calculate the absolute differences between each element in the sliced dataList and the target number
        differences = [abs(element - target_number) for element in sliced_data]

        # Find the index of the element with the minimum absolute difference
        min_difference_index = differences.index(min(differences))

        # Get the element and its index in the original dataList
        #nearest_element = sliced_data[min_difference_index]
        nearest_index = start_index + min_difference_index

        num6 = float(nearest_index/60)

        formatted_number1 = "{:.1f}".format(num1)
        formatted_number2 = "{:.1f}".format(num2)
        formatted_number3 = "{:.1f}".format(num3)
        formatted_number4 = "{:.1f}".format(num4)
        formatted_number5 = "{:.1f}".format(num5)
        formatted_number6 = "{:.1f}".format(num6)
        formatted_number7 = "{:.1f}".format(num7)
        formatted_number10 = "{:.1f}".format(num10)

        flabel1.config( text="" +str(formatted_number1), borderwidth=3, relief="groove", width=25,font=16)
        root.update()

        flabel2.config( text=""+str(formatted_number2), borderwidth=3, relief="groove", width=25,font=16)
        root.update()

        flabel3.config(text=""+str(formatted_number3), borderwidth=3, relief="groove", width=25,font=16)
        root.update()

        flabel4.config( text=""+str(formatted_number4), borderwidth=3, relief="groove", width=25,font=16)
        root.update()

        flabel5.config( text=""+str(formatted_number5), borderwidth=3, relief="groove", width=25,font=16)
        root.update()
     
        flabel6.config( text=""+str(formatted_number6), borderwidth=3, relief="groove", width=25,font=16)
        root.update()
     
        flabel7.config( text=""+str(formatted_number7), borderwidth=3, relief="groove", width=25,font=16)
        root.update()
        
        flabel10.config(text=""+str(formatted_number10), borderwidth=3, relief="groove", width=25,font=16)
        root.update()


        with open('project_bombc.csv', 'w') as file:
            for data_item, y_item in zip(yList, dataList):
                file.write(f"{data_item},{y_item}\n")

        
        sc = ax.scatter(yList[fo], dataList[fo])
        scc=ax.scatter(yList[300],dataList[300])
        sm = ax.scatter(yList[nearest_index], dataList[nearest_index])
        highlight_circle = plt.Circle((yList[fo], dataList[fo]), 0.1, color='#3B444B', fill=True)
        highlight_circlec = plt.Circle((yList[300], dataList[300]), 0.1, color='#3B444B', fill=True)
        highlight_circlem = plt.Circle((yList[nearest_index], dataList[nearest_index]), 0.1, color='#3B444B', fill=True)
        ax.add_patch(highlight_circle)
        ax.add_patch(highlight_circlec)
        ax.add_patch(highlight_circlem)

        plt.gca().set_facecolor('white')
        plt.show()

        
        
                
    
    ani = animation.FuncAnimation(fig, animate, frames=1700, interval=1000)       

    # Create a frame for the GUI elements
    gui_frame = Frame(root,bg="#54626F")
    gui_frame.pack(side="left", fill="both" )

    
     # ... your other GUI code remains the same ...
    
    

    def animo():
        
        ani._start()
        canvas1 = FigureCanvasTkAgg(fig, root)  # Use root as parent for canvas
        canvas1.draw()
        canvas1.get_tk_widget().pack(side="right", fill="both", expand=True)



    # Create entry boxes for the numbers
    label1 = Label(gui_frame, text="Value of tc:", borderwidth=3, relief="groove",width=30,font=16)
    label2 = Label(gui_frame, text="Value of ta:", borderwidth=3, relief="groove", width=30,font=16)
    label3 = Label(gui_frame, text="Value of r1:", borderwidth=3, relief="groove", width=30,font=16)
    label4 = Label(gui_frame, text="Value of r2:", borderwidth=3, relief="groove", width=30,font=16)
    label5 = Label(gui_frame, text="Value of a:", borderwidth=3, relief="groove", width=30,font=16)
    label6 = Label(gui_frame, text="Value of b:", borderwidth=3, relief="groove", width=30,font=16)
    label7 = Label(gui_frame, text="Value of c:", borderwidth=3, relief="groove", width=30,font=16)
    label8 = Label(gui_frame, text="Length of the burnt wire (cm):", borderwidth=3, relief="groove", width=30,font=16)
    label9 = Label(gui_frame, text="Mass of the coal (g):", borderwidth=3, relief="groove", width=30,font=16)
    label10 = Label(gui_frame, text="Energy Equivalent of calorimeter:", borderwidth=3, relief="groove", width=30,font=16)
    label11 = Label(gui_frame, text="",bg="gray")#for a gap in between result and calculate button

    flabel1 = Label(gui_frame, text="", borderwidth=3, relief="groove", width=25,font=16)
    flabel2 = Label(gui_frame, text="", borderwidth=3, relief="groove", width=25,font=16)
    flabel3 = Label(gui_frame, text="", borderwidth=3, relief="groove", width=25,font=16)
    flabel4 = Label(gui_frame, text="", borderwidth=3, relief="groove", width=25,font=16)
    flabel5 = Label(gui_frame, text="", borderwidth=3, relief="groove", width=25,font=16)
    flabel6 = Label(gui_frame, text="", borderwidth=3, relief="groove", width=25,font=16)
    flabel7 = Label(gui_frame, text="", borderwidth=3, relief="groove", width=25,font=16)
    entry8 = Entry(gui_frame, width=25, borderwidth=3, relief="groove",font=16)
    entry9 = Entry(gui_frame, width=25, borderwidth=3, relief="groove",font=16)                                                                                        
    flabel10 = Label(gui_frame, text="", borderwidth=3, relief="groove", width=25,font=16)
   
  
    # Function to calculate and display the sum
    def calculate():
        global num1;
        global num2;
        global num3;
        global num4;
        global num5;
        global num6;
        global num7;
        global num10;
        try:
            num8=float(entry8.get())
            num9=float(entry9.get())
            numo=float(num1-num2-num3*(num6-num5)-num4*(num7-num6))
            sum_value = float(1.8*(num10*numo-num8*2.3)/num9)
            formatted_result = "{:.1f}".format(sum_value)
            result_label.config(text="The calorific value of the coal is (Btu/lb): " + str(formatted_result),font=("Arial", 16, "bold"))
        except ValueError:
            result_label.config(text="Invalid input. Please enter numbers.",font=("Helvetica", 18, "bold"))

    def tm():
        global start_time
        start_time=time.time()
        button_st.config(state=DISABLED)
        animo()

    # Create a button to trigger the calculation
    
    button_st = Button(gui_frame, text="Start",font=("Arial", 15, "bold"),width=30,height=5,bg="#A1CAF1",command=tm)#************have to add the animo function here as command************************
    button = Button(gui_frame, text="Calculate", command=calculate,font=("Arial", 16, "bold"))
   

    # Create a label to display the result
    result_label = Label(gui_frame, text="Result:", borderwidth=3,font=("Arial", 16, "bold"))

    # Arrange the widgets in the window
    button_st.grid(row=0,column=0,columnspan=2)

    label1.grid(row=1, column=0)
    label2.grid(row=2, column=0)
    label3.grid(row=3, column=0)
    label4.grid(row=4, column=0)
    label5.grid(row=5, column=0)
    label6.grid(row=6, column=0)
    label7.grid(row=7, column=0)
    label8.grid(row=8, column=0)
    label9.grid(row=9, column=0)
    label10.grid(row=10, column=0)
    flabel1.grid(row=1, column=1)
    flabel2.grid(row=2, column=1)
    flabel3.grid(row=3, column=1)
    flabel4.grid(row=4, column=1)
    flabel5.grid(row=5, column=1)
    flabel6.grid(row=6, column=1)
    flabel7.grid(row=7, column=1)

    entry8.grid(row=8, column=1)
    entry9.grid(row=9, column=1)

    flabel10.grid(row=10, column=1)


    button.grid(row=11, column=1,pady=20)
    label11.grid(row=12,column=0) #for a gap in between result and calculate button
    result_label.grid(row=13, column=0,columnspan=2)



# Initialize opacities
 # Start text at a slightly lower opacity

# Create labels for the image and text
image_label = Label(root)
image_label.pack()

#text_label = Label(root, text="Bombcalorimeter", font=("Helvetica", 30))
#text_label.pack()

# Start the fading effect
fade_image_and_text()
#time.sleep(10)

wel_fr = Frame(root,bg="#54626F")
#wel_fr.pack_propagate(False)*********************************************************


# Welcome message label
welcome_label = Label(wel_fr, text="Welcome to Our Application!", font=("Arial", 40),width=30)
  # Add padding

text_labelin = Label(wel_fr,padx=20 ,text="INSTRUCTIONS:\n***For details see the Instruction Manual.\n\n1.Check if the Arduino board is connected to your PC's 'COM4' port.\n2.You Can check this from the 'Device Manager' of your PC.\n3.If it is not 'COM4' then change it to 'COM4'.\n4.To change: Device Manager→Ports (COM & LPT)→Arduino\n   →Right-Click and Select 'Properties'→Port Settings→Advanced→Choose COM4→OK\n5.Use Display Scale as 125%.",font=("Arial", 20),justify="left")


#labelac = Label(wel_fr, text="Acknowledgment\nDr. Kazi Arafat Rahman, Associate Professor\nPriom Das, Lecturer\nShahriar Alam, Lecturer\nSakib Javed, Lecturer", bg="#f4f1bb",font=("Arial", 20))


labelid = Label(wel_fr,width=30, text="Created by Team 'CG-5' \n Abrar Jahin\n Ariful Haque Faruky\n Muhibur Rahaman Fuadh\n Sadman Hasan Sadaf", bg="#f4f1bb",font=("Arial", 20))



# Button to proceed
proceed_button = Button(wel_fr, text="Enter",font=("Arial", 25), command= appo)

#sys.exit()

#sys.exit()
root.mainloop()
