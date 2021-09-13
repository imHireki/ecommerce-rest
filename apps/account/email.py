from djoser import email


class ActivationEmail(email.ActivationEmail):
    """ Overriding the account activation with a html template """
    template_name = 'account/activation.html'
