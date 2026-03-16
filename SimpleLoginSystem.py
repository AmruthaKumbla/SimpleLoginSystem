# BACKEND CODE

LOGINDETAILS_FILE = "logindetails.txt"

def user_details(username, password):
    with open(LOGINDETAILS_FILE, "a") as f:    #open in append mode so that previous data won't get vanished
        f.write(f"{username},{password}\n")   

def read_user_details():   
    users = {}
    import os                               #imports os module(used to check if file exists)
    if not os.path.exists(LOGINDETAILS_FILE):
        return users                        #if file is not there,it returns empty dict
                                            #(so that if file does not exist it doesn't crash and returns empty file) 
    try:                                    #If something goes wrong in this block it won't crash ,instead goes to except block

        with open(LOGINDETAILS_FILE, "r") as f:     
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",", 1)  #splits at the first comma
                                            #(we use this so even if there is comma in password it only splits after username)
                if len(parts) != 2:
                    continue
                user, pw = parts
                users[user] = pw
    except Exception:
        users = {}
    return users

def check_login(username, password):   #Return (True, message) or (False, message)
    
    users = read_user_details()   
    if not username or not password:
        return False, "Please enter BOTH Username and Password"

    if username in users and users[username] == password:
        return True, "Login Successful!"

    return False, "Invalid username or password"       #runs when username does not exist OR password is wrong

def create_user(username, password):   #"""Return (True, message) or (False, message)."""
    users = read_user_details()        
    if not username or not password:
        return False, "Please enter BOTH Username and Password"
    if username in users:
        return False, "Username already exists"
    try:
        user_details(username, password)
    except Exception:
        return False, "Failed to save credentials"
    return True, "Account created successfully"


# FRONTEND CODE


import wx
window=wx.App()                                                      #starts the gui
frame=wx.Frame(None,title="Simple login system",size=(700,700))     #creates the frame
pan=wx.Panel(frame,style=wx.SIMPLE_BORDER)                                                  #creates the panel where widgets can be placed
pan.SetBackgroundColour("white")


text1= wx.StaticText(pan, label="Account Login",pos=(720,150))
text2 = wx.StaticText(pan, label="User Name : ",pos=(400,300))
text3 = wx.StaticText(pan, label="Password : ",pos=(400,350))
btn1 = wx.Button(pan, label="Login", pos=(1025,450),size=(75,30))                        #for the final login
btn2=wx.Button(pan,label="Create Account",pos=(400,450),size=(120,30))


usebox=wx.TextCtrl(pan,pos=(600,300),size=(500,30))                                     #creates the box for username
passbox=wx.TextCtrl(pan,pos=(600,350),size=(500,30),style=wx.TE_PASSWORD)              #creates the box for password

checkpass = wx.CheckBox(pan, label="Show Password", pos=(1000,400))                       # Create checkbox                                                                                        
                                                                                       

def show_password(event):
    global passbox                                            #nside the function, if you assign a new value to passbox without global, Python treats it as a new local variable.
    value = passbox.GetValue()                                #gets the current text typed in the password box
    pos = passbox.GetInsertionPoint()                          # This remembers where the cursor is so after hiding or showing the password, you can put the cursor back in the same place.

    if checkpass.GetValue():
        style = 0                                                   # Show password as normal text
    else:
        style = wx.TE_PASSWORD                                       # Hide password (dots)

    # Destroy old TextCtrl and create a new one
    passbox.Destroy()
    passbox = wx.TextCtrl(pan, pos=(600,350), size=(500,30), style=style)    
    passbox.SetValue(value)                               # sets the value given by the user
    passbox.SetInsertionPoint(pos)                         #inserts the cursor point
    passbox.SetFont(font5)                                  #sets the same font back
    pan.Refresh()                                              #ensures the new TextCtrl is displayed correctly, so the password visibility change happens instantly.

checkpass.Bind(wx.EVT_CHECKBOX,show_password)

font5 = wx.Font(14, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)    #increases the size of the input text  
usebox.SetFont(font5)                                                              
passbox.SetFont(font5)


font1=text1.GetFont()                                               #this gets the font style of text1
font1.SetPointSize(20)                                             #sets the fontsize to the given value
text1.SetFont(font1)                                                #basically executes it


font2=text2.GetFont() 
font2.SetPointSize(14)
text2.SetFont(font2)


font3=text3.GetFont()
font3.SetPointSize(14)
text3.SetFont(font3)

font4=btn1.GetFont()
font4.SetPointSize(14)
btn1.SetFont(font4)


font6=btn2.GetFont()
font6.SetPointSize(12)
btn2.SetFont(font6)

  
def Onpaint(event):                                        #to draw a rectangle
    dc=wx.PaintDC(pan)
    dc.SetPen(wx.Pen("black",2))
    dc.SetBrush(wx.Brush("light blue"))
    dc.DrawRectangle(300,100,1000,500)

    

pan.Bind(wx.EVT_PAINT,Onpaint)

#Add event handlers

def on_login_click(event):
    username = usebox.GetValue().strip()
    password = passbox.GetValue()
    ok, msg = check_login(username, password)        
    if ok:
        wx.MessageBox(msg, "Login", wx.OK|wx.ICON_INFORMATION)   #used to customize the MessageBox.
                                                                 #It tells the message box to show an information icon(blue circle with "i").
    else:
        wx.MessageBox(msg, "Login Failed", wx.OK|wx.ICON_ERROR)  #Shows a red error icon.

def on_create_click(event):
    username = usebox.GetValue().strip()
    password = passbox.GetValue()
    ok, msg = create_user(username, password)        
    if ok:
        wx.MessageBox(msg, "Account", wx.OK|wx.ICON_INFORMATION)
    else:
        wx.MessageBox(msg, "Account Creation Failed", wx.OK|wx.ICON_ERROR)





btn1.Bind(wx.EVT_BUTTON, on_login_click) #When user clicks btn1 (Login button), Run on_login_click
btn2.Bind(wx.EVT_BUTTON, on_create_click)#When user clicks btn2 (Create Account button), Run on_create_click()




frame.Show()
window.MainLoop()
