from core import *
import matplotlib.pyplot as plt
import numpy as np

def create_graph(fname, assignment, scores):
    graph_scores = []
    for name, score in scores:
        graph_scores.append(score)
    graph_scores = sorted(graph_scores)
    x = np.arange(len(scores))
    fig, ax = plt.subplots()
    plt.bar(x, graph_scores)
    plt.xticks(x)
    plt.title(assignment)
    plt.savefig(fname)

def query():
    # User input for the grade/student files.
    gfile = input('Grade file: ')
    sfile = input('Student file: ')
    # Creating the readers
    gr = GradeReader(gfile)

    assignments = gr.get_assignment_names()
    print('\nAvailable assignments: ', *assignments, sep='\n\t')

    assignment = input('\nAssignment: ')
    while assignment not in assignments:
        print('Invalid Assignment.')
        assignment = input('Assignment: ')

    scores = gr.get_scores(assignment)
    empty = gr.are_empty(scores)
    if not empty:
        a = Analyzer(scores)
        a.show_scores()
        save = input('Would you like to save this data?(y/n): ')
        if save.lower() == 'y':
            fname = input('File name: ')
            create_graph(fname, assignment, scores)
            print("Data Saved as {}.png".format(fname))
        else:
            exit()

    else:
        print('Scores not ready for this assignment.')
 
def notify_students():
    # User input for the grade/student files.
    gfile = input('Grade file: ')
    sfile = input('Student file: ')
    # Creating the readers
    gr = GradeReader(gfile)
    sr = StudentReader(sfile)

    assignments = gr.get_assignment_names()
    print('\nAvailable assignments: ', *assignments, sep='\n\t')

    assignment = input('\nAssignment: ')
    while assignment not in assignments:
        print('Invalid Assignment.')
        assignment = input('Assignment: ')

    scores = gr.get_scores(assignment)
    empty = gr.are_empty(scores)
    if not empty:
        a = Analyzer(scores)
        studentScores = a.student_scores(sr.students)

        #Creating Data and Emailer
        e = Emailer('Emailer')
        fname = input('Save graph file as: ')
        create_graph(fname, assignment, scores)
        print('Data saved, sending out email to your students.')

        #Sending each student a personalized email.
        for student, score in studentScores:
            message = "Hello, {}. \nNew grades for {} have been posted.\n".format(student.fname, assignment)
            message += "\nSome data:\n"
            message += a.censored_scores()
            message += "\nYou scored a {}.".format(score)

            if student.formatted_name() in a.getMinNames():
                message += "\nYou're falling behind, email me!"
            elif student.formatted_name() in a.getMaxNames():
                message += "\nGreat job!"

            subject = 'Grade Update!'
            e.send_email(student.email, subject, message, fname)

    else:
        print('Scores not ready for this assignment.')
        exit()

def main():
    print('Welcome to Grade Emailer')
    print('Commands: Query, Notify Students\n\t[q, ns]')
    command = input('Command: ').lower()
    while command not in ['q', 'ns']:
        print("Invalid Command.")
        command = input('Command: ')
    if command == 'q':
        query()
    else:
        notify_students()

if __name__ == "__main__":
    main()
