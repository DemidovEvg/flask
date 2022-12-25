def plural_word(num, text_form_zerro, text_form_one, text_form_two):
    num = abs(num) % 100
    num1 = num % 10
    if 10 < num < 20:
        return text_form_zerro
    if 1 < num1 < 5:
        return text_form_two
    if num1 == 1:
        return text_form_one
    return text_form_zerro
