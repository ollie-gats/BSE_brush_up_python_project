
import random
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')


def daily_infection(starting_infected: int, infection_probability: float, max_infections: int = 3) -> int:
    """Models daily infection

    Args:
        starting_infected (int): Number of people initially infected
        infection_probability (float): Probability of infection
        max_infections (int): Maximum number of people a person can infect

    Returns:
        int: Total number of people infected at the end of the day
    """
    
    extra_infected = 0
    for infected_person in list(range(0, starting_infected)):
        encounter = 0
        while encounter < max_infections:
            if random.random() < infection_probability:
                extra_infected += 1
            encounter += 1
    return extra_infected + starting_infected



def infection_model(number_days: int, starting_infected: int, infection_probability: float) -> pd.DataFrame:
    """Models disease spread over multiple days

    Args:
        number_days (int): Number of days to model over
        starting_infected (int): Number of people initially infected
        infection_probability (float): Probability of infection

    Returns:
        pd.DataFrame: Dataframe with number of infected people on each day
    """
    
    infected_df = pd.DataFrame(
        {'Day': [0],
         'Infected': [starting_infected]}
    )
    
    for day in list(range(1, number_days+1)):
        day_infection = daily_infection(infected_df['Infected'][len(infected_df)-1], infection_probability)
        day_reading = {'Day': day, 'Infected': day_infection}
        infected_df.loc[len(infected_df)] = day_reading
        
    return infected_df

       

def full_pop_infected(population: int, starting_infected: int, infection_probability: float) -> pd.DataFrame:
    """Models the length of time for a full population to become infected

    Args:
        population (int): Total population
        starting_infected (int): Number of people initially infected
        infection_probability (float): Probability of infection

    Returns:
        pd.DataFrame: Dataframe with number of infected people on each day
    """
    
    infected_df = pd.DataFrame(
        {'Day': [0],
         'Infected': [starting_infected]}
    )
    
    day = 1
    
    while infected_df['Infected'][len(infected_df)-1] < population:
        day_infection = daily_infection(infected_df['Infected'][len(infected_df)-1], infection_probability)
        if day_infection < population:
            day_reading = {'Day': day, 'Infected': day_infection}
        else:
            day_reading = {'Day': day, 'Infected': population}
        infected_df.loc[len(infected_df)] = day_reading
        day += 1
    
    print('Model estimates ' + str(day) + ' days until the full population is infected.')
    
    return infected_df
    


def vaccine_introduction(starting_infected: int, vaccine_day: int, vaccine_effectiveness: float,
                        number_days: int, infection_probability: float) -> pd.DataFrame:
    """Models the introduction of a vaccine

    Args:
        starting_infected (int): Number of people initially infected
        vaccine_day (int): Day vaccine is introduced
        vaccine_effectiveness (float): Amount vaccine reduces infection probability by
        number_days (int): Number of days to model over
        infection_probability (float): Probability of infection

    Returns:
        pd.DataFrame: Dataframe with number of infected people on each day
    """
    infected_df = pd.DataFrame(
        {'Day': [0],
         'Infected': [starting_infected]}
    )
    
    day = 1  
    for day in list(range(1, number_days+1)):
        if day < vaccine_day:
            day_infection = daily_infection(infected_df['Infected'][len(infected_df)-1], infection_probability)
        else:
            day_infection = daily_infection(infected_df['Infected'][len(infected_df)-1], infection_probability-vaccine_effectiveness)
        
        day_reading = {'Day': day, 'Infected': day_infection}
        infected_df.loc[len(infected_df)] = day_reading
        day += 1
    
      
    print("With a vaccine on day " + str(vaccine_day) + " the model estimates there will be " +\
        str(infected_df['Infected'][len(infected_df)-1]) + " people infected on day " + str(number_days))
        
    return infected_df


def plot_pandemic(df: pd.DataFrame, infected_col: str, vaccine_day: int = None) -> None:
    """Plots the development of a pandemic

    Args:
        df (pd.DataFrame): Dataframe with information on the number of people infected on each day
        infected_col (str): Column containing infected data
        vaccine_day (int, optional): Day of vaccine introduction. Defaults to None.
    """
    fig, ax = plt.subplots()
    ax.plot(df[infected_col])
    ax.set_xlabel('Days')
    ax.set_ylabel('Number of infected')
    ax.set_title('Disease transmission')
    
    if vaccine_day:
        ax.axvline(x=vaccine_day, color='green', linestyle='--', label='Vaccine introduction')
        plt.legend()
    
    plt.show()


# Simulation over 3 days
three_day_sim = infection_model(3, 10, 0.05)
plot_pandemic(three_day_sim, 'Infected')

# How long for full pop to be infected?
full_pop_sim = full_pop_infected(1000, 10, 0.05)
plot_pandemic(full_pop_sim, 'Infected')

# Vaccine introduction
vaccine_sim = vaccine_introduction(10, 3, 0.01, 10, 0.05)
plot_pandemic(vaccine_sim, 'Infected', 3)

