# made by tyrant (it is jank, i know)
import fractions
from math import pi,inf
import textwrap
from tkinter import *
from tkinter import ttk
from PIL import ImageTk,Image
import os
class Body:
    """A Celestial Body in the Game Kerbal Space program.
    This can refer to the sun, Kerbol, each of its Planets,and all of their moons.
    
Attributes
----------
A name, an equatorial radius/sea level (metres), gravitational parameter, 
sphere of influence (metres), sidereal rotation period (seconds), 
atmospheric depth (metres)."""
    def __init__(
        self,
        name,
        Equatorial_radius,
        gravitational_parameter,
        sphere_of_influence,
        sidereal_rotation_period,
        Atmosphere_depth
        ):
        self.name=name
        self.Equatorial_radius=Equatorial_radius
        self.gravitational_parameter=gravitational_parameter
        self.SOI=sphere_of_influence
        self.period=sidereal_rotation_period
        self.atmos=Atmosphere_depth
Kerbol=Body("Kerbol",261600000,1.1723328e18,inf,432000,600000)
Moho=Body("Moho",250000,1.6860938e11,9646663,2215754,0)
Eve=Body("Eve",700000,8.1717302e12,85109365,80500,90000)
Gilly=Body("Gilly",13000,8289449.8,126123,28255,0)
Kerbin=Body("Kerbin",600000,3.5316e12,84159286,21549.425,70000)
Mun=Body("Mun",200000,6.5138398e10,2429559.1,138984.38,0)
Minmus=Body("Minmus",60000,1.7658e9,2247428.4,40400,0)
Duna=Body("Duna",320000,3.0136321e11,47921949,65517.859,50000)
Ike=Body("Ike",130000,1.8568369e10,1049598.9,65517.862,0)
Dres=Body("Dres",138000,2.1484489e10,32832840,34800,0)
Jool=Body("Jool",6000000,2.82528e14,2.4559852e9,36000,200000)
Laythe=Body("Laythe",500000,1.962e12,3723645.8,52980.879,50000)
Vall=Body("Vall",300000,2.074815e11,2406401.4,105962.09,0)
Tylo=Body("Tylo",600000,2.82528e12,10856518,211926.36,0)
Bop=Body("Bop",65000,2.4868349e9,1221060.9,544507.43,0)
Pol=Body("Pol",44000,7.2170208e8,1042138.9,901902.62,0)
Eeloo=Body("Eeloo",210000,7.4410815e10,1.1908294e8,19460,0)
Celestial_Bodies={Kerbol,Moho,Eve,Gilly,Kerbin,Mun,Minmus,Duna,Ike,Dres,Jool,Laythe,Vall,Tylo,Bop,Pol,Eeloo}

Target=Kerbol
root=Tk()
root.title("Orbital Calculator")
root.iconbitmap("Kerbal.ico")
# this makes the window
def changeimage(*args):
    """this function changes the BodyImage object to match the current Target. 
Requires all the prerequisite planetgifs to be in the directory.
\nChanges global values instead of returning values."""
    global Target, BodyImage,img
    img=ImageTk.PhotoImage(Image.open(Target.name+".gif"))
    BodyImage.itemconfigure(BodyImage.create_image(100,100,anchor=CENTER,image=img),image=img)
    BodyImage.create_image(100,100,anchor=CENTER,image=img)
def changetarget(event):
    """Change the Target object to match that of a celestial body. 
Target and Celestial_Bodies use class type 'Body'.
\nChanges global values instead of returning values.
    
Parameters
----------
event : the selected value of the combobox"""
    global Target,Planetinfo,Planetary_name_var,Planetary_SOI_var,Planetary_Synchro_var,Planetary_SemiSynchro_var,which_planet
    for i in Celestial_Bodies:
        if i.name==event.widget.get().replace(" ",""):
            Target=i
    Planetary_name_var.set(f"Name: {Target.name}")
    Planetary_SOI_var.set(f"Sphere of Influence: {Target.SOI/1000:,} Km")
    Planetary_Synchro_var.set(autotextwrapper(cansynchro(Target),40))
    Planetary_SemiSynchro_var.set(autotextwrapper(cansemisynchro(Target),40))
    Planetary_radius_var.set(f"Radius: {Target.Equatorial_radius/100:,} Km")
    which_planet=body_list_combobox.get()
    changeimage()
    calculation()
def greyout(*args):
    """Deactivates the Entry Boxes underneath the inactive Radiobuttons. 
    For instance, when height is selected, the period boxes deactivate. 
    Returns no value, only changes global variables.
    """
    global period_or_height,HeightInput,HeightInput_var,HoursInput,HoursInput_var,MinutesInput,MinutesInput_var,SecondsInput,SecondsInput_var
    if period_or_height.get()=="Height":
        HeightInput.state(['!disabled'])
        HoursInput_var.set("0")
        HoursInput.state(['disabled'])
        MinutesInput_var.set("0")
        MinutesInput.state(['disabled'])
        SecondsInput_var.set("0")
        SecondsInput.state(['disabled'])
    elif period_or_height.get()=="Period":
        HeightInput_var.set("0")
        HeightInput.state(['disabled'])
        HoursInput.state(['!disabled'])
        MinutesInput.state(['!disabled'])
        SecondsInput.state(['!disabled'])
def calculation(*args):
    """Converts data from Orbital Period to Orbital Height and Vice versa.
    \nThe core of the application
    \nChanges global values instead of returning values."""
    global period_or_height,Target,HeightInput_var,HoursInput_var,MinutesInput_var,SecondsInput_var
    h=0
    p=0
    if HeightInput_var.get()=="":
        HeightInput_var.set("0")
    if HoursInput_var.get()=="":
        HoursInput_var.set("0")
    if MinutesInput_var.get()=="":
        MinutesInput_var.set("0")
    if SecondsInput_var.get()=="":
        SecondsInput_var.set("0")
    if period_or_height.get()=="Height":
        try:
            h=1000*float(HeightInput_var.get())
            p=hrsminsecstr(orbitperiod(h))
        except:
            pass
        else:
            h=1000*float(HeightInput_var.get())
            p=hrsminsecstr(orbitperiod(h))
            segments=secondstohours(orbitperiod(h))
            HoursInput_var.set(format(round(segments[0]),","))
            MinutesInput_var.set(round(segments[1]))
            SecondsInput_var.set(round(segments[2],2))
    elif period_or_height.get()=="Period":
        try:
            p=hourstoseconds(int(HoursInput_var.get()),int(MinutesInput_var.get()),float(SecondsInput_var.get()))
            h=orbitheight(p)
        except:
            pass
        else:
            p=float(HoursInput_var.get())*3600+float(MinutesInput_var.get())*60+float(SecondsInput_var.get())
            h=orbitheight(p)
            HeightInput_var.set(format(round(h/1000,2),","))
            p=hrsminsecstr(p)
    else:
        pass
    if h>Target.SOI:
        SOI_check=f",but is outside of {Target.name}'s Sphere of Influence."
    else:
        SOI_check="."
    if h<0:
        heightcheck=",but is below ground"
    elif h<Target.atmos:
        heightcheck=",but is inside the atmosphere"
    else:
        heightcheck=""
    finalstring=autotextwrapper(f"A circular orbit of {round(h/1000,4):,} Km around {Target.name} takes {p} to complete{heightcheck}{SOI_check}",60)
    result.set(finalstring)
def secondstohours(seconds):
    """Turns input of x seconds into a list of numbers in the form [hours, minutes,seconds]
    
Parameters
----------
x : A large quantity of seconds (int/float)

Returns
-------
[hours,minutes,seconds] : a list of type int,int,int/float"""
    return [
        seconds//3600,
        seconds//60-(seconds//3600)*60,
        seconds%3600-(seconds//60-(seconds//3600)*60)*60]
def hourstoseconds(hours:int,mins:int,secs):
    """Takes a list of three numbers [hours,minutes,seconds] and turns them into pure seconds
    
Parameters
----------
[hours,minutes,seconds] : a list in the form int/float,int/float,int/float.
    Minutes and seconds do not have to be below 60.
    
Returns
-------
x : A large quantity of seconds"""
    return hours*3600+mins*60+secs
def hrsminsecstr(seconds):
    """Takes a number of seconds and turns it into a string in the following style:
'x hours, y minutes, and z seconds'.

Parameters
----------
x : large quantity of seconds, can be float or int

Returns
-------
output : A string in the following form:
    'a hours, b minutes, and c seconds'."""
    y=secondstohours(seconds)
    return f"{str(round(y[0]))} hours, {str(round(y[1]))} minutes, and {str(round(y[2],2))} seconds"
def orbitperiod(metres):
    """Takes an input height (in metres above sea level) and turns it into an orbital period.
    
Parameters
----------
x : An integer or float, in metres above sea level.
    This represents the orbital height for a circular orbit
    The distance is measured from sea level, not the body's centre.

Returns
-------
period : A float, in seconds.
    This represents the orbital period for a circular orbit at that height."""
    global Target
    return 2*pi*((((metres+Target.Equatorial_radius)**3)/Target.gravitational_parameter)**(1/2))
def orbitheight(seconds):
    """Takes an input period (in seconds) and turns it into an orbital height (in metres above sea level).
    
Parameters
----------
x : An integer or float, in seconds.
    This represents the orbital period for a circular orbit.

Returns
-------
period : A float, in metres above sea level.
    This represents the orbital height for a circular orbit at that period."""
    global Target
    return (((seconds**2)*Target.gravitational_parameter/(4*pi**2))**(1/3))-Target.Equatorial_radius
def cansynchro(T:Body):
    """Returns a string in the form:
    \n'Synchronous orbit is/is not possible around target'"""
    if orbitheight(T.period)>T.SOI or orbitheight(T.period)<T.atmos:
        truefalse="not "
        bonustext="."
    else:
        truefalse=""
        bonustext=f"at a height of {round(orbitheight(T.period)/1000):,} km and a period of {hrsminsecstr(T.period)}."
    return f"Synchronous orbit is {truefalse}possible around {T.name}{bonustext}"
def cansemisynchro(T:Body):
    """Returns a string in the form:
    \n'Semi-synchronous orbit is/is not possible around target'"""
    if orbitheight((T.period)/2)>T.SOI or orbitheight(T.period/2)<T.atmos:
        truefalse="not "
        bonustext="."
    else:
        truefalse=""
        bonustext=f"at a height of {round(orbitheight(T.period/2)/1000):,} km and a period of {hrsminsecstr(T.period/2)}."
    return f"Semi-synchronous orbit is {truefalse}possible around {T.name}{bonustext}"
def update_satellites(*args):
    """Changes the Information on the Satellite output label. 
    Returns no value, only changes global variables."""
    global SatelliteOutput_var,number_of_satellites_var,HoursInput_var,MinutesInput_var,SecondsInput_var
    fraction1=(int(number_of_satellites_var.get())-1)/int(number_of_satellites_var.get())
    fraction2=(int(number_of_satellites_var.get())+1)/int(number_of_satellites_var.get())
    p=float(HoursInput_var.get())*3600+float(MinutesInput_var.get())*60+float(SecondsInput_var.get())
    SatelliteOutput_var.set(autotextwrapper(
        f"The ideal insertion orbit for {number_of_satellites_var.get()} satellites are as follows:"+
        f"{hrsminsecstr(p*fraction1)} for a smaller insertion orbit,"+
        f"and {hrsminsecstr(p*fraction2)} for a larger insertion orbit.",
    25)
    )
def autotextwrapper(value:str,length:int):
    """Automatically returns a new string with line breaks automatically inserted

Parameters
----------
value : The string to be wrapped
length : The number of characters allowed per line

Returns
-------
wrapped text : A string with newlines inserted at the appropriate places."""
    return textwrap.TextWrapper(width=length).fill(text=value)
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N,E,S,W))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
# this allows the window to be resized without looking jank
# ---------------------the left column
leftcolumn=ttk.Frame(mainframe)

# the image of the celestial body
BodyImage=Canvas(
    leftcolumn,
    width=200,
    height=200)

planet_Labelframe=ttk.Labelframe(
    leftcolumn,
    text="Pick a Celestial Body")

# planet selection combobox
which_planet=StringVar(root,"Kerbol")
body_list_combobox=ttk.Combobox(
    planet_Labelframe,
    textvariable=which_planet)
body_list_combobox['values']=(
    'Kerbol','Moho','Eve','   Gilly','Kerbin','   Mun','   Minmus','Duna','   Ike',
    'Dres','Jool','   Laythe','   Vall','   Tylo','   Bop','   Pol','Eeloo'
)
body_list_combobox.state(["readonly"])
body_list_combobox.current(0)
body_list_combobox.bind("<<ComboboxSelected>>",func=changetarget)

Planetinfo=ttk.Labelframe(
    leftcolumn,
    text="Info:",
    width=270,
    height=160)

Planetary_name_var=StringVar(root,value=f"Name: {Target.name}")
Planetary_name=ttk.Label(
    Planetinfo,
    textvariable=Planetary_name_var,
    justify="left")

Planetary_radius_var=StringVar(root,value=f"Radius: {Target.Equatorial_radius/100:,} Km")
Planetary_radius=ttk.Label(
    Planetinfo,
    textvariable=Planetary_radius_var,
    justify="left")

Planetary_SOI_var=StringVar(root,value=f"Sphere of Influence: {Target.SOI/1000:,} Km")
Planetary_SOI=ttk.Label(
    Planetinfo,
    textvariable=Planetary_SOI_var,
    justify="left")

Planetary_Synchro_var=StringVar(root,value=autotextwrapper(cansynchro(Target),40))
Planetary_Synchro=ttk.Label(
    Planetinfo,
    textvariable=Planetary_Synchro_var,
    justify="left")

Planetary_SemiSynchro_var=StringVar(root,value=autotextwrapper(cansemisynchro(Target),40))
Planetary_SemiSynchro=ttk.Label(
    Planetinfo,
    textvariable=Planetary_SemiSynchro_var,
    justify="left")

# ----------------------middle column
# this radiobutton picks between period and height
middlecolumn=ttk.Frame(mainframe)
Enter_value=ttk.Labelframe(
    middlecolumn,
    text="Enter Data")
period_or_height=StringVar(value="Period")
period_radiobutton=ttk.Radiobutton(
    Enter_value,
    text="Enter Orbital Period",
    variable=period_or_height,
    value="Period",
    command=greyout)
height_radiobutton=ttk.Radiobutton(
    Enter_value,
    text="Enter Orbital Height",
    variable=period_or_height,
    value="Height",
    command=greyout)
# these entry field does the calculations
HeightInput_var=StringVar()
HeightInput=ttk.Entry(
    Enter_value,
    textvariable=HeightInput_var)
HoursInput_var=StringVar()
HoursInput=ttk.Entry(
    Enter_value,
    textvariable=HoursInput_var)
MinutesInput_var=StringVar()
MinutesInput=ttk.Entry(
    Enter_value,
    textvariable=MinutesInput_var)
SecondsInput_var=StringVar()
SecondsInput=ttk.Entry(
    Enter_value,
    textvariable=SecondsInput_var)
# this bit below initialises the boxes
HeightInput_var.set("0")
HeightInput.state(['disabled'])
HoursInput.state(['!disabled'])
MinutesInput.state(['!disabled'])
SecondsInput.state(['!disabled'])

# this part is the output
output_box=ttk.Labelframe(
    middlecolumn,
    text="Result:")
result=StringVar(value=autotextwrapper(f"A circular orbit of 0 Km takes 0 hours, 0 minutes and 0 seconds to complete",60))
calculation_output=ttk.Label(
    output_box,
    textvariable=result,
    justify="left")

# this part is the Satellite stuff
SatelliteFrame=ttk.Labelframe(
    middlecolumn,
    text="Satellite Insertion Options:")
number_of_satellites_var=StringVar()
number_of_satellites=ttk.Spinbox(
    SatelliteFrame,
    textvariable=number_of_satellites_var,
    from_=2,
    to=12,
    command=update_satellites)
number_of_satellites.state(['readonly'])
SatelliteOutput_var=StringVar(value=autotextwrapper("Please select a number of satellites.",30))
SatelliteOutput=ttk.Label(
    SatelliteFrame,
    textvariable=SatelliteOutput_var,
    justify="left")

satelliteimage=Canvas(
    SatelliteFrame,
    width=200,
    height=200
)
# -----------------------Right column
# rightcolumn=ttk.Labelframe(mainframe,text="Satellite Insertion Calculator")
# turns out i didn't need this right column

# ---------------------------------------------------------gridding
leftcolumn.grid(column=0,row=0)
# all the things in the left column are below here:
planet_Labelframe.grid(column=0,row=0)
body_list_combobox.grid(column=0,row=0)

BodyImage.grid(column=0,row=1)
img=ImageTk.PhotoImage(Image.open("Kerbol.gif"))
BodyImage.create_image(100,100,anchor=CENTER,image=img)

Planetinfo.grid(column=0,row=2,sticky=(N))
Planetary_name.grid(column=0,row=0,sticky=(W))
Planetary_radius.grid(column=0,row=1,sticky=(W))
Planetary_SOI.grid(column=0,row=2,sticky=(W))
Planetary_Synchro.grid(column=0,row=3,sticky=(W))
Planetary_SemiSynchro.grid(column=0,row=4,sticky=(W))


middlecolumn.grid(column=1,row=0,sticky=(N))
# all the things in the middle column are below here:
Enter_value.grid(column=0,row=0,sticky=(N))
period_radiobutton.grid(column=0,row=0,columnspan=2)
HoursInput.grid(column=0,row=1)
ttk.Label(Enter_value,text="hours").grid(column=1,row=1)
MinutesInput.grid(column=0,row=2)
ttk.Label(Enter_value,text="minutes").grid(column=1,row=2)
SecondsInput.grid(column=0,row=3)
ttk.Label(Enter_value,text="seconds").grid(column=1,row=3)
# right column of Enter_value labelframe is below here
height_radiobutton.grid(column=2,row=0,columnspan=2)
HeightInput.grid(column=2,row=1)
ttk.Label(Enter_value,text="Km").grid(column=3,row=1)

output_box.grid(column=0,row=1,sticky=(N))
calculation_output.grid(column=0,row=0)

SatelliteFrame.grid(column=0,row=3)
number_of_satellites.grid(column=0,row=0,sticky=NW)
SatelliteOutput.grid(column=0,row=1,sticky=N)

img2=ImageTk.PhotoImage(Image.open("Satellite.gif"))
satelliteimage.create_image(0,0,anchor=NW,image=img2)
satelliteimage.grid(column=1,row=0,rowspan=2)
# rightcolumn.grid(column=3,row=0)
# i planned on having three columns but then realised i didn't need the third

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
# a bit of polish to give the thing some padding, apparently

HeightInput_var.trace_add("write", calculation)
HoursInput_var.trace_add("write", calculation)
MinutesInput_var.trace_add("write", calculation)
SecondsInput_var.trace_add("write", calculation)

root.resizable(width=False, height=False)
root.mainloop()