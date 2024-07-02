from functions import (
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
    #   height (list): List of height values. It must be of length equal to N.
    #   left_x (list): List of left_x values. It must be of length equal to N.
    #   right_x (list): List of right_x values. It must be of length equal to N.
    N = 22
    water_amount_per_unit_of_length = 1.

    height = [18, 90, 86, 17, 12, 81, 33, 77, 57, 89, 33, 60, 18, 6,  68, 23, 65, 62, 72,  5, 91, 86 ]
    left_x = [28,  9, 63, 37, 15, 76, 36, 12, 53, 53, 48, 57, 23, 11, 13, 52, 25, 18, 30, 21,  5, 12 ]
    right_x = [46, 18, 76, 39, 32, 89, 47, 44, 67, 57, 54, 58, 27, 24, 31, 70, 38, 31, 43, 36, 18, 62 ]

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