# monte carlo for monty hall
from asyncio.proactor_events import _ProactorBaseWritePipeTransport
from random import sample
from turtle import onclick
import matplotlib.pyplot as plt

def runMontyHall(num_doors = 3, swap = True, verbose = False):
    # initialize the doors
    doors = set(range(num_doors))
    
    # randomly select the guess and the winning door
    winning_door = sample(doors, 1)[0]
    guess = sample(doors, 1)[0]

    if swap: # if we swap, calculate feasible doors to open before the swap
        greg = {guess, winning_door}
        valid_shown_doors = doors - greg
        #shown_doors = sample(valid_shown_doors, len(valid_shown_doors) - 1) if len(valid_shown_doors) > 1 else valid_shown_doors 

        if winning_door == guess:
            remaining_door = sample(valid_shown_doors, 1)[0]
        else:
            remaining_door = winning_door

        if verbose:
            print(f"doors = {doors}")
            print(f"winning_door = {winning_door}")
            print(f"guess = {guess}")
            print(f"valid_shown_doors = {valid_shown_doors}")
            #print(f"shown_doors = {set(shown_doors)}")
            #print(f"guess = {guess}")
            print(f"swapped from {guess} to {remaining_door}")
            print("---------------------")

        return remaining_door == winning_door, guess == winning_door



    return guess == winning_door

def runMonteCarlo(num_trials = 1e5, num_doors = 3, swap = True, verbose = False, plot = True):
    num_trials = int(num_trials)

    outputs_swap = []
    outputs_no_swap = []

    if plot:
        plt.ion()
        fig, ax = plt.subplots()
        asymptote_val = (num_doors-1)/num_doors if swap else 1 - (num_doors-1)/num_doors
        line, = ax.plot([], [], 'b-', label = 'Cumulative success rate: SWAP')
        line2, = ax.plot([], [], 'g-', label = 'Cumulative success rate: NO SWAP')
        ax.axhline(asymptote_val, color = 'r', label = f'swap asymptote val = {round(asymptote_val, 4)}')
        ax.axhline(1-asymptote_val, color = 'r', label = f'no swap symptote val = {round(1-asymptote_val, 4)}')
        ax.set_xlim(0, num_trials)
        ax.set_ylim(0, 1)
        plt.xlabel("Trial Number")
        plt.ylabel("Success Rate")
        ax.legend()

        def on_close(event):
            plt.close(fig)
        
        fig.canvas.mpl_connect('close_event', on_close)

    for x in range(num_trials):
        trial_outcome = runMontyHall(num_doors, swap, verbose)
        outputs_swap.append(trial_outcome[0])
        outputs_no_swap.append(trial_outcome[1])


        if plot:
            if not plt.fignum_exists(fig.number):
                break

            success_rate = sum(outputs_swap)/len(outputs_swap)
            line.set_data(range(len(outputs_swap)), [sum(outputs_swap[:i+1])/(i+1) for i in range(len(outputs_swap))])
            line2.set_data(range(len(outputs_no_swap)), [sum(outputs_no_swap[:i+1])/(i+1) for i in range(len(outputs_no_swap))])

            if len(outputs_swap) > 1: # rescale axis
                ax.set_xlim(0, len(outputs_swap))
                ax.set_ylim(0, max(1, success_rate + 0.1))

            plt.draw()
            plt.pause(0.0001)

            ax.set_title(f'Monte Carlo Simulation for {num_doors} Door Monty Hall:\n Winning {round(100*sum(outputs_swap)/len(outputs_swap), 2)}% of the time with SWAP={swap}')
    plt.ioff()
    plt.show()

    #print(outputs)
    return sum(outputs_swap)/len(outputs_swap)

def main():
    num_trials = 1e5
    num_doors = 3
    swap = True
    verbose = False
    plot = True

    out = runMonteCarlo(num_trials, num_doors, swap, verbose, plot)
    print(f'The successful outcome occured {round(100*out, 6)} percent of the time')
    return -1

if __name__ == '__main__':
    main()