def spam_check(messages, items, chat_id, sub_user):
    for i in range(0, items):
        for t in range(i, items):
            if (messages[i][0] == messages[t][0]):
                if (messages[i][2] != messages[t][2]):
                    for g in range(t, items):
                        if (messages[t][0] == messages[g][0]):
                            if (messages[t][2] != messages[g][2]):
                                spam_user = messages[i][1]
                                spam_user_name = sub_user.get_user_info(spam_user).nickname
                                
                                all_users_name = sub_user.get_chat_users(chat_id).nickname
                                if spam_user_name in all_users_name:
                                    sub_user.kick(spam_user, chat_id, True)
                                    print(f'{spam_user_name} исключён из чата')
