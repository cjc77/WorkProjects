import matplotlib.pyplot as plt


def make_pie(data_dict, chart_title):
    # Get rid of k/v pairs where v is 0 => 0%
    new_data_dict = {k: v for k, v in data_dict.items() if v != 0}

    labels = list(new_data_dict.keys())
    sizes = list(new_data_dict.values())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct="%.1f%%", shadow=True,
           startangle=10)
    plt.title(chart_title, y=1.1)
    ax.axis("equal")

    plt.show()


def make_bar(data_dict, x_title, y_title, chart_title):
    pos = range(len(data_dict))
    width = 0.5
    a = .5
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_title(chart_title)
    ax.set_ylabel(x_title)
    ax.set_xlabel(y_title)

    # Create bar char with response counts
    plt.bar(pos, data_dict.values(), width, alpha=a, align="center")
    plt.xticks(range(len(data_dict)), data_dict.keys())
    plt.show()
