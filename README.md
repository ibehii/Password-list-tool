# **Password list tool**
![](https://skillicons.dev/icons?i=py,vscode,md)

With this script you can :
- [Generate one password](#generate-one-password)
- [Generate password list](#generate-password-list)
- [Sort password list](#sort-password-list)
- [Delete duplicate passwords in password list](#delete-duplicate-passwords-in-password-list)
- [Merge password lists](#merge-password-lists)
---
# Dependencies 
This program use [**pyfiglet**](https://pypi.org/project/pyfiglet/) and [**colorama**](https://pypi.org/project/colorama/) as external library.\
By running the program this libraries will be downloaded, but if there were any problem you can install them manually by following command :\
> for install colorama : `pip install colorama`\
> for install pyfiglet : `pip install pyfiglet`  

![](https://user-images.githubusercontent.com/79264026/178007880-62568118-e073-4c17-8946-8c19808293fd.png)
Also program need [ANSI Shadow](https://github.com/xero/figlet-fonts/blob/master/ANSI%20Shadow.flf) that will be downloaded after running program

---
# YouTube Tutorial
![](https://youtu.be/hlkBS0gWI7g)
---
# Generate One Password
In this part you can generate one password quickly.
It's really good for signing up in sites or apps when you want use strong password.\
![]()
Also after generating the password it will be save in a **json** file, so you can access it later by: -> running program -> Just one password -> Show previous passwords
![](screenshot)

In this menu you can choose what characters you want in the password.\
When you want to enter number of your choices, pay attention that numbers must be between **1-5** -> `1 2 5` \
And use **spaces** when you want to separate 

![](screenshot)

In this menu you choose length of password. For example if you enter **8** the script will return a password with 8 characters. like -> `12345678`

![](screenshot)
We save the passwords that you generate in **Just_one_password.json** file.

---
# Generate password list
In this part you can generate passwords and export it as txt file.

![](screenshot)
In this menu you can choose what characters you want in the password.\
When you want to enter number of your choices, pay attention that numbers must be between **1-5** -> `1 2 5` \
And use **spaces** when you want to separate 

![](screenshot)

In this menu you choose **number** of password that script will generate. In second question you choose length of password. For example if you enter **8** the script will return a password with 8 characters. like -> `12345678`

---
# sort password list
On this part you can sort your password list. For example if your password is like this `125, 142, 111` it will change to -> `111, 125, 142` .

![](screenshot)

Only thing that you must do is enter name of your file :)\
**If you get "file is not exists. Enter file name correctly !" error but you are sure that file exist try to enter complete path of file**
## finding complete path
In windows:
> Right click the file then choose copy as a path option\

![]()

In linux:
> use "pwd" command and add file name at the end of it

---
# delete duplicate passwords in password list
If one password is repeated in password list this part of program will delete it and keep just one of them.

![](screenshot)
On this menu we have two method **slow method** and **fast method**.

**Slow method** use more memory and it's take long time to delete duplicates, but it doesn't disrupts the order of password list .

**Fast method** It's much faster than slow mood but only problem is that it disrupts the order of your password list. 
if you don't care about the order of your file use this method and then sort it with [sort password list](#sort-password-list) part.

**If you get "file is not exists. Enter file name correctly !" error but you are sure that file exist try to enter complete path of file**

[**Explanation for finding complete path**](#finding-complete-path)

---
# Merge password lists
In this part of program you can merge your password lists and make your password lists into single file.
![](screenshot)

**If you get "file is not exists. Enter file name correctly !" error but you are sure that file exist try to enter complete path of file**

[**Explanation for finding complete path**](#finding-complete-path)
 