import sys
from visdom import Visdom

d = {}  # holds all our graphs
viz = Visdom()

def get_line(x, y, name, color='#000', isFilled=False, fillcolor='transparent', width=2, showlegend=False):
    if isFilled:
        fill = 'tonexty'
    else:
        fill = 'none'

    return dict(
        x=x,
        y=y,
        mode='lines',
        type='custom',
        line=dict(
            color=color,
            width=width),
        fill=fill,
        fillcolor=fillcolor,
        name=name,
        showlegend=showlegend
    )

def plot_error(epoch, error, name, xaxis, color='#000'):
    win = name
    title = name

    if name not in d:
        d[name] = []
    d[name].append((epoch, error)) # this might need some work

    x, y = zip(*d[name]) # need to understand this
    data = [get_line(x, y, 'error', color=color)]

    layout = dict(
        title=title,
        xaxis={'title': xaxis},
        yaxis={'title': title}
    )

    viz._send({'data': data, 'layout': layout, 'win': win})


def plot(x, y, xaxis, data_type, name, color='#000', refresh=True):
    # create dictionary spots if they don't already exist
    if data_type not in d:
        d[data_type] = {}
    if name not in d[data_type]:
        d[data_type][name] = {'points': [], 'color': color}

    # if given a single number, save its float
    if not isinstance(y, (float, int)):
        if len(y.shape) == 0:
            y = float(y)
            # if given a set of numbers, save their mean and confidence interval info
        else:
            y = y.cpu()
            mean, std = y.mean().item(), 3.291 * y.std().item() / sqrt(len(y))
            lower, upper = mean - std, mean + std
            y = (lower, mean, upper)

    # save the modified data
    d[data_type][name]['points'].append((x, y))

    # the actua plotting
    if refresh:
        win = data_type
        title = data_type
        data = []
        for name in d[data_type]:
            x, y = zip(*d[data_type][name]['points'])

            # if extracting mean and confidence internval info, plot the mean with error shading
            if isinstance(y[0], tuple):
                lower, mean, upper = zip(*y)
                data.append(get_line(x, lower, name, color='transparent'))
                data.append(get_line(x, upper, name, color='transparent', isFilled=True, fillcolor=d[data_type][name]['color'] + '44'))
                data.append(get_line(x, mean, name, color=d[data_type][name]['color'], showlegend=True))
            # if extracting single values, plot them as a single line
            else:
                data.append(get_line(x, y, name, color=d[data_type][name]['color'], showlegend=True))

        layout = dict(
            title=title,
            xaxis={'title': xaxis},
            yaxis={'title': data_type}
        )

        viz._send({'data': data, 'layout': layout, 'win': win})
