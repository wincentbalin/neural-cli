import neuralnet
import numpy as np
import click
import writer

writer = writer.Writer()

@click.group()
def cli():
    pass

@click.command(options_metavar='<options>')
@click.option("--lam", type=click.FLOAT, default=1, help="The regularization amount [default 1]")
@click.option("--maxiter", default=250, type=click.INT, help="The maximum iterations for chosen to minimise the cost function [default 250]")
@click.option("--output", type=click.STRING, help="A file path to save the minimised parameters to")
@click.option("--normalize", default=True, type=click.BOOL, help="Perform normalization on the training set [default true]")
@click.option("--verbose", default=True, type=click.BOOL, help="Output the training progress [default true]")
@click.argument("X", type=click.File('rb'))
@click.argument("Y", type=click.File('rb'))
def train(x, y, output, lam, maxiter, normalize, verbose):
    """Train a neural network with the given X and Y parameters.
    
    Arguments:\n
        [X] must be a file path to a CSV which holds your training data\n
        [Y] must be a file path to a CSV which holds your expected outputs for the training examples

    (neural cli will ommit the first row for column headers for both CSVs)
    """
    X = np.loadtxt(x, delimiter=",",skiprows=1, dtype="float")
    Y = np.loadtxt(y, delimiter=",",skiprows=1, dtype="float")

    nn = neuralnet.NeuralNet(X=X, Y=Y, writer=writer, output=output, lam=lam, maxiter=maxiter, norm=normalize)
    nn.train(verbose=verbose, save=output)
    nn.accuracy()

@click.command(options_metavar='<options>')
@click.argument("sizei", type=click.INT)
@click.argument("sizeh", type=click.INT)
@click.argument("labels", type=click.INT)
@click.argument("params", type=click.File('rb'))
@click.option("--normalize", type=click.BOOL, help="Perform normalization on the training set [default true]")
def predict(sizei, sizeh, labels, params, normalize):
    """
    predict an output with a given row
    
    Arguments:\n
        [sizei] the size of the input layer that the parameters were trained on \n
        [sizeh] the size of the hidden layer that the parameters were trained on \n
        [labels] the size of the output layer that the parameters were trained on \n
        [params] the file that holds a 1 * n rolled parameter vector \n
    """

    X = np.loadtxt(training, delimiter=",",skiprows=1, dtype="float")
    Y = np.loadtxt(expected, delimiter=",",skiprows=1, dtype="float")

    x = np.loadtxt(x, delimiter=",",skiprows=0, dtype="float")
    nn = neuralnet.NeuralNet(X=X, Y=Y, writer=writer)

    nn.set_params(np.loadtxt(params, delimiter=",",skiprows=0, dtype="float"))
    print nn.predict(x[np.newaxis])

@click.command(options_metavar='<options>')
@click.option("--lam", type=click.FLOAT, default=1, help="The regularization amount [default 1]")
@click.option("--maxiter", default=250, type=click.INT, help="The maximum iterations for chosen to minimise the cost function [default 250]")
@click.option("--output", type=click.File('rb'), help="A file path to save the minimised parameters to")
@click.option("--normalize", default=True, type=click.BOOL, help="Perform normalization on the training set [default true]")
@click.option("--step", default=10, type=click.INT, help="The increments that the training will increase the set by [default 10]")
@click.argument("X", type=click.File('rb'))
@click.argument("Y", type=click.File('rb'))
def test(training, x, y, output, lam, maxiter, normalize, step):
    """Test the given network on the train and validation sets
    
    Arguments:\n
        [X] must be a file path to a CSV which holds your training data\n
        [Y] must be a file path to a CSV which holds your expected outputs for the training examples

    (neural cli will ommit the first row for column headers for both CSVs)
    """

    X = np.loadtxt(x, delimiter=",",skiprows=1, dtype="float")
    Y = np.loadtxt(y, delimiter=",",skiprows=1, dtype="float")

    nn = neuralnet.NeuralNet(X=X, Y=Y, writer=writer, output=output, lam=lam, maxiter=maxiter)
    nn.test(step)


cli.add_command(test)
cli.add_command(predict)
cli.add_command(train)

if __name__ == '__main__':
    cli()