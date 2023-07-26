from Controller import ControllerPessoa

controller = ControllerPessoa()

while True:
    opcao = int(input('MENU\n'
                  '1 - Login\n'
                  '2 - Cadastro\n'
                  '3 - Sair\n'))
    
    if opcao == 1:
        email = input('Email: ')
        senha = input('Senha: ')
        controller.login(email, senha)

    elif opcao == 2:
        nome = input('Nome: ')
        email = input('Email: ')
        senha = input('Senha: ')
        controller.cadastro(nome, email, senha)

    elif opcao == 3:
        break

    else:
        print('Opção inválida!')