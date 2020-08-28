from email_report import connect_email, send_email
#import templates 
#from email_report import make_report

# end user owns this function
def make_random_figure():
    data =  np.random.normal(size=(20, 2))
    df = DataFrame(data, columns=['Goldfish Sales','Stock_Index_Price'])
    df['Stock_Index_Price'] += 10
    return df

# this will eventually be in email_project.py
def make_report(figure_list, title_list, caption_list, theme='green_theme'):

    # get html template from template directory
    # we need to move the html template to the templates folder
    html_path = 'templates/{}.html'
    html_file = open(html_path, 'r')
    html_template = html_file.read()
    html_file.close()

    # make report from list of figures/titles/captions
    for figure, title, caption in zip(figure_list, title_list, caption_list):
        
        # html_block = some combination of figure, title, caption

        html_block_template = "this is a string {0} \n figure here: \n {1} \n caption: {2}"
        # html_block = html_block_template.format(title, figure, caption)
     
        # insert this block into the main template (called html_report)
 
    return html_report



if __name__ == "__main__":

    figure_list = [make_random_figure() for i in range(4)]
    title_list = ['a', 'b', 'c', 'd']
    caption_list = ['aa', 'bb', 'cc', 'dd']
    report = make_report(figure_list, title_list, caption_list)

    subject = 'just practice'
    message = 'hi everyone'
    
    # connection = connect_email(username, pwd, etc)
    # send_email(connection, subject, message, report, recipient_email)
    
