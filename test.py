from functions import (
    generate_random_drains,
    validate_input,
    calculate_drain_amount,
    generate_raindrops,
    process_to_height_and_raindrops,
    plot_graph,
)

if __name__ == "__main__":

    DISPLAY_PLOT = True

    # ---------------------------------------------------------------------------
    # INPUTS
    # ---------------------------------------------------------------------------
    # Please insert/replace your inputs here below:
    #   N (int): Number of drains to generate. N is a positive integer.
    #   water_amount_per_unit_of_length (float): Amount of water per unit of length. Must be positive.
    #   wall_left_x (int): Left x-coordinate of the wall.
    #   wall_right_x (int): Right x-coordinate of the wall.
    #   wall_minimum_height (int): Minimum height of the wall.
    #   wall_maximum_height (int): Maximum height of the wall.
    #   maximum_n_drains_per_height (int, optional): Maximum number of drains per height. Defaults to 3.
    #   seed_value (int, optional): Seed value for reproducible random generation. Defaults to None.
    N = 20
    water_amount_per_unit_of_length = 1.0
    
    wall_left_x = 10
    wall_right_x = 40  
    wall_minimum_height = 10  
    wall_maximum_height = 100
    maximum_n_drains_per_height = 5
    seed_value = 1

    height, left_x, right_x = generate_random_drains(
        N=N,
        wall_left_x=wall_left_x,
        wall_right_x=wall_right_x,
        wall_minimum_height=wall_minimum_height,
        wall_maximum_height=wall_maximum_height,
        maximum_n_drains_per_height=maximum_n_drains_per_height,
        seed_value=seed_value,
    )

    # ---------------------------------------------------------------------------
    # INPUT VALIDATION
    # ---------------------------------------------------------------------------
    validate_input(
        height=height,
        left_x=left_x,
        right_x=right_x,
        N=N,
        water_amount_per_unit_of_length=water_amount_per_unit_of_length,
    )

    # ---------------------------------------------------------------------------
    # RESOLUTION ALGORITHM
    # ---------------------------------------------------------------------------
    df = calculate_drain_amount(
        N=N,
        height=height,
        left_x=left_x,
        right_x=right_x,
        water_amount_per_unit_of_length=water_amount_per_unit_of_length,
    )
    drain_amounts = df["drain_amount"].to_list()

    # Printing the drain amounts
    print(drain_amounts)

    # ---------------------------------------------------------------------------
    # GRAPHICAL OUTPUT
    # ---------------------------------------------------------------------------
    if DISPLAY_PLOT:

        # ------------------------------------------
        # RANDOM RAIN DROPS GENERATION
        # ------------------------------------------
        # Replace:
        #   num_drops (int): Number of rain drops
        #   seed_value (int, optional): Seed value for random number generator. Default is None.
        # with your desired values.
        num_drops = 10000
        seed_value = 0
        rain_drops_x, rain_drops_y = generate_raindrops(
            num_drops=num_drops,
            x_min=min(left_x),
            x_max=max(right_x),
            y_min=min(height),
            y_max=max(height),
            seed_value=seed_value,
        )

        # ------------------------------------------
        # TO_HEIGHT AND RAINDROPS EVALUATION
        # ------------------------------------------
        df, rain_drops_x, rain_drops_y = process_to_height_and_raindrops(
            N=N, df=df, rain_drops_x=rain_drops_x, rain_drops_y=rain_drops_y
        )

        # ------------------------------------------
        # PLOT
        # ------------------------------------------
        plot_graph(df=df, rain_drops_x=rain_drops_x, rain_drops_y=rain_drops_y)