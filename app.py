import os
from collections import OrderedDict
from uuid import uuid4

from flask import Flask, render_template
from flask import flash, request, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/tmp/'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app = Flask(__name__)


def get_key_position(first_line, delimeter, key):
    columns = first_line.split(delimeter)
    for i in range(0, len(columns)):
        if columns[i] == key:
            return i
    AssertionError("provided column does not exist in the provided data")


def work(distribution, number):
    # print("{} {} {} {}", number, len(number), number[0], number[0].isdigit())
    if len(number) > 0 and number[0].isdigit():
        first = int(number[0])
        oldCount = distribution.get(first, 0)
        distribution[first] = oldCount + 1
        return True
    return False


def plat_graph(distribution, total_lines, total_parsed_ines, valid):
    # print("total lines {} data {}".format(totalLines, distribution))
    labels = distribution.keys()
    values = distribution.values()
    return render_template('bar_chart.html', title='Distribution', totalLines=total_lines,
                           totalParsedLines=total_parsed_ines, valid=valid, labels=labels,
                           values=values, max=max(values))


def validate_law(sort_distribution):
    for i in range(2, 9):
        if sort_distribution[i - 1] is not None and sort_distribution[i] is not None \
                and sort_distribution[i - 1] < sort_distribution[i]:
            return False
    return True


@app.route("/", methods=['GET', 'POST'])
def index():
    try:
        if request.method == 'POST':
            file = request.files['file']
            key = request.form['key']
            delimiter = request.form['delimiter']
            if delimiter is not None and len(delimiter) > 0 and delimiter == "space":
                delimiter = ' '
            else:
                delimiter = '\t'
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                filename = secure_filename(str(uuid4()) + file.filename)
                path = os.path.join(UPLOAD_FOLDER, filename)
                file.save(path)
                return parse(delimiter, key, path)
        else:
            return render_template('input.html')
    except:
        return render_template('invalid.html')


def parse(delimiter, key, path):
    with open(path) as f:
        first_line = f.readline()
        keyColumnNumber = get_key_position(first_line, delimiter, key)
        distribution = {}
        totalLines = 0
        total_parsed_lines = 0
        for line in f:
            # print(line)
            totalLines = totalLines + 1
            splitLine = line.split(delimiter)
            if len(splitLine) >= keyColumnNumber:
                number = splitLine[keyColumnNumber]
                if work(distribution, number):
                    total_parsed_lines = total_parsed_lines + 1
    sort_distribution = OrderedDict(sorted(distribution.items()))
    valid = validate_law(sort_distribution)
    return plat_graph(sort_distribution, totalLines, total_parsed_lines, valid)


if __name__ == "__main__":
    app.run()
