# **Password list tool**
![](https://skillicons.dev/icons?i=py,vscode,md)

This script is a password list manager that you can :
- [Generate one password](#generate-one-password)
- [Generate password list](#generate-password-list)
- [Sort password list](#sort-password-list)
- [Delete duplicate passwords in password list](#delete-duplicate-passwords-in-password-list)
- [Merge password lists](#merge-password-lists)
- [Check password strength]()
---
# Dependencies 
This program use [**pyfiglet**](https://pypi.org/project/pyfiglet/), [**colorama**](https://pypi.org/project/colorama/), [**tqdm**](https://pypi.org/project/tqdm/) and [**zxcvbn**](https://pypi.org/project/zxcvbn/) as external library.\
By running the program these libraries will be downloaded, but if there are any problems you can install them manually by following the command :
> pip install -r requirements.txt
---
# YouTube Tutorial
https://youtu.be/hlkBS0gWI7g
---
# Generate One Password
![Screenshot from 2023-07-06 13-14-50](https://github.com/beh185/Password-list-tool/assets/79264026/e7749da4-97b7-4568-b64d-9417fbb78a1a) 

In this part, you can generate one password quickly.
It's really good for signing up on sites or apps when you want to use a strong password.

![Screenshot from 2023-07-06 13-16-26](https://github.com/beh185/Password-list-tool/assets/79264026/99195d0b-15bc-4ac7-a108-4575c8476f1b)


Also after generating the password it will be saved in a **json** file, so you can access it later by: -> running program -> Just one password -> Show previous passwords


![Screenshot from 2023-07-06 13-16-51](https://github.com/beh185/Password-list-tool/assets/79264026/9abe8fbf-33aa-4c6d-ab6f-150d7b8c5e59)

In this menu, you can choose what characters you want in the password.\
When you want to enter the number of your choices, pay attention that numbers must be between **1-5** -> `1 2 5` \
And use **spaces** when you want to separate 

![Screenshot from 2023-07-06 17-16-36](https://github.com/beh185/Password-list-tool/assets/79264026/afe1a5a5-a51e-458d-8387-6e802cec3e75)

In this menu, you choose the length of the password. For example, if you enter **8** the script will return a password with 8 characters. like -> `12345678`

We save the passwords that you generate in the **one_password.json** file.

---
# Generate password list
In this part, you can generate passwords and export them as a txt file.

![Screenshot from 2023-07-06 13-19-16](https://github.com/beh185/Password-list-tool/assets/79264026/17150533-900e-41bd-b08e-cc0da697b49c)


In this menu, you can choose what characters you want in the password.\
When you want to enter the number of your choices, pay attention that numbers must be between **1-5** -> `1 2 5` \
And use **spaces** when you want to separate 


![Screenshot from 2023-07-06 13-19-52](https://github.com/beh185/Password-list-tool/assets/79264026/b80461bb-cce8-4587-acc5-06a84d6a4160)

In this menu, you choose the **number** of the password that the script will generate. In the second question, you choose the length of the password. For example, if you enter **8** the script will return a password with 8 characters. like -> `12345678`

---
# Sort password list

![Screenshot from 2023-07-06 13-20-28](https://github.com/beh185/Password-list-tool/assets/79264026/07a7b1a6-0439-4203-8145-d414cb518408)

On this part, you can sort your password list. For example, if your password is like this `125, 142, 111` it will change to -> `111, 125, 142`.

The only thing that you must do is enter the name of your file :)\
**If you get the "file does not exist. Enter file name correctly !" error but you are sure that the file exists try to enter the complete path of the file**
## Finding a complete path
In Windows:
> Right-click the file then choose copy as a path option\

![select_copy_as_path](https://github.com/beh185/Password-list-tool/assets/79264026/1e22bdb7-b6b3-4bd8-95b8-c993899b058c)


In Linux:
> Use "pwd" command and add the file name at the end of it

---
# Delete duplicate passwords in the password list
If a password is repeated in the password list, this section will delete it and keep just one of them.

![Screenshot from 2023-07-06 13-20-50](https://github.com/beh185/Password-list-tool/assets/79264026/131a58c3-e3ee-4bf0-9cac-d23e1dc6f19a)


**Method 1** is a little bit slower than method 2, but it doesn't disrupt the order of the password list.

**Method 2** It's faster than method 1 but the only problem is that it disrupts the order of your password list. 
if you don't care about the order of your file use this method and then sort it with the [sort password list](#sort-password-list) part.

**If you get the "file does not exist. Enter file name correctly !" error but you are sure that the file exists try to enter the complete path of the file**

[**Explanation for finding complete path**](#finding-complete-path)

---
# Merge password lists

![Screenshot from 2023-07-06 13-22-16](https://github.com/beh185/Password-list-tool/assets/79264026/8591be6d-e4d7-4cba-854e-f0599a02c099)

In this section, you can merge your password lists and make your password lists into a single file.

**If you get the "file does not exist. Enter file name correctly !" error but you are sure that the file exists try to enter the complete path of the file**

[**Explanation for finding complete path**](#finding-complete-path)
 
