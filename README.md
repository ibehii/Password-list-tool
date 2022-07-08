# **Password list tool**
![](https://skillicons.dev/icons?i=py,vscode,md)

With this script you can :
- [Generate one password](#generate-one-password)
- [Generate multiple password](#generate-multiple-password)
- [sort password list](#sort-password-list)
- [delete duplicate passwords in password list](#delete-duplicate-passwords-in-password-list)
- [add password lists together](#add-password-lists-together)
---
# Dependencies 
This script use [**pyfiglet**](https://pypi.org/project/pyfiglet/) and [**colorama**](https://pypi.org/project/colorama/) so you need to install them with these commands :\
for install colorama : `pip install colorama`\
for install pyfiglet : `pip install pyfiglet`  

![](screenshot)
Also pyfiglet need [ANSI Shadow](https://github.com/xero/figlet-fonts/blob/master/ANSI%20Shadow.flf) font but you don't need to install it, When you run script if you don't have the font it will install.

---
# Generate one password
In this part you can generate one password quickly.
It's good for sign up in site or app that you want use strong password and then save password somewhere .
![](screenshot)

In this menu you can choose which characters be on you password. Enter number of your choice like this -> `1 2 5` \
if you want to separate the number use space. if you use anything else you will get error.

![](screenshot)

In this menu you choose length of password. For example if you enter **8** the script will return a password with 8 characters. like -> `12345678`

![](screenshot)
Also we save the password that you generate in hidden file name `.Just_one_password.txt`. you can access to your previous password in the end of **generate one password** part

---
# Generate multiple password
In this part you can generate passwords and export it as txt file. Actually you are creating password list.

![](screenshot)
This part is like [Generate one password](#generate-one-password). In this menu you can choose which characters be on you passwords. Enter number of your choice like this -> `1 2 5` \
if you want to separate the number use space. if you use anything else you will get error.

![](screenshot)

In this menu you choose **number** of password that script will generate. In second question you choose length of password. For example if you enter **8** the script will return a password with 8 characters. like -> `12345678`

---
# sort password list
On this part you can sort your password list. For example if your password is like this `125, 142, 111` it will change to -> `111, 125, 142` .

![](screenshot)

Only thing that you must do is enter name of your file :)\
Remember that if your file is not in same directory of terminal enter complete path of your password list.\
For example :  I'm running terminal in `/home/user/` directory but the password list is in `/home/user/Desktop/` so in script i must enter `/home/user/Desktop/Your_file_name`.\
but if I'm running terminal in `/home/user/` and my password list is in there too, I just need to enter name of the password list

---
# delete duplicate passwords in password list
If one password is repeated in password list this part of script will delete it and keep just one of them.

![](screenshot)
On this menu we have to meted **slow** and **fast**.

**Slow mood** use more memory and it's take long time to delete duplicates. but it's stable and it doesn't disrupts the order of password list .

**Fast mood** It's much faster than slow mood but only problem is it's disrupts the order of your password list. 
if you don't care about the order of your file use this meted and then sort it with [sort password list](#sort-password-list) part.

---
# add password lists together
In this part of script you can add your password lists together and make your password lists into single file.
![](screenshot)
 