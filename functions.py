import pandas as pd
import numpy as np
from typing import Tuple
import matplotlib.pyplot as plt


def generate_random_drains(
    N: int,
    wall_left_x: int,
    wall_right_x: int,
    wall_minimum_height: int,
    wall_maximum_height: int,
    maximum_n_drains_per_height: int = 3,
    seed_value: int = None,
) -> Tuple[list, list, list]:
    """
    Generate random rain drain coordinates based on given parameters.

    Args:
        N (int): Number of rain drains to generate.
        wall_left_x (int): Left x-coordinate of the wall.
        wall_right_x (int): Right x-coordinate of the wall.
        wall_minimum_height (int): Minimum height of the wall.
        wall_maximum_height (int): Maximum height of the wall.
        maximum_n_drains_per_height (int, optional): Maximum number of drains per height. Defaults to 3.
        seed_value (int, optional): Seed value for reproducible random generation. Defaults to None.

    Returns:
        Tuple[list, list, list]: Lists containing heights, left x-coordinates, and right x-coordinates of generated rain drains.
    """
    if (type(N) != int) or (N <= 0):
        raise Exception("N must be a positive integer.")

    if (type(seed_value) != int) or (seed_value < 0):
        if (seed_value) == None:
            pass
        else:
            raise Exception("seed_value must be an integer greater than or equal to 0.")

    if (type(maximum_n_drains_per_height) != int) or (maximum_n_drains_per_height <= 1):
        raise Exception(
            "maximum_n_drains_per_height must be a positive integer greater than 1."
        )

    if (
        (type(wall_right_x) != int)
        or (type(wall_left_x) != int)
        or (wall_right_x <= wall_left_x)
    ):
        raise Exception(
            "The right x-coordinate of the wall (wall_right_x) and the left x-coordinate (wall_left_x) must be integers. In particular, wall_right_x must be greater than wall_left_x."
        )

    if (
        (type(wall_maximum_height) != int)
        or (type(wall_minimum_height) != int)
        or (wall_maximum_height <= wall_minimum_height)
    ):
        raise Exception(
            "The wall maximum height (wall_maximum_height) and the wall minimum height (wall_minimum_height) must be integers. In particular, wall_maximum_height must be greater than wall_minimum_height."
        )

    count = 0
    height = []
    left_x = []
    right_x = []

    if seed_value is not None:
        np.random.seed(seed_value)

    seed_value_list = np.random.randint(0, N, N)

    while count != N:
        flag = True

        # We use the same seed value at each step to achieve reproducibility.
        np.random.seed(seed_value_list[count])

        while flag:

            # Random generation of a new height coordinate
            height_coordinate = np.random.randint(
                wall_minimum_height, wall_maximum_height, 1
            )[0]

            # If we already generated rain drains for that specific height coordinate we move to another height coordinate
            if height_coordinate not in height:
                flag = False

        # Number of rain drains at the chosen height coordinate
        n_drains_per_height = np.random.randint(1, maximum_n_drains_per_height, 1)[0]

        # We generate distinct random x-coordinates to avoid overlapping among the rain drains
        x_coordinates = np.sort(
            np.random.choice(
                range(wall_left_x, wall_right_x), 2 * n_drains_per_height, replace=False
            )
        )

        height += [int(height_coordinate)] * (len(x_coordinates) // 2)
        count += len(x_coordinates) // 2

        for i, component in enumerate(x_coordinates):
            if i % 2 == 0:
                left_x += [int(component)]
            else:
                right_x += [int(component)]

        if count >= N:
            height = height[:N]
            left_x = left_x[:N]
            right_x = right_x[:N]
            break

        if set(height) == set(range(wall_minimum_height, wall_maximum_height)):
            raise Exception(
                "Too many rain drains to fit in the specified wall. Please change the inputs given to the function."
            )

    return height, left_x, right_x


def validate_input(
    height: list,
    left_x: list,
    right_x: list,
    N: int,
    water_amount_per_unit_of_length: float,
):
    """
    Validate input lists for correct dimensions and data types.

    Args:
        height (list): List of height values.
        left_x (list): List of left_x values.
        right_x (list): List of right_x values.
        N (int): Expected length of the input lists. N is a positive integer.
        water_amount_per_unit_of_length (float): the amount of water/length that is flowing down from the top edge of the wall

    Raises:
        Exception: If input lists have incorrect dimensions or data types.
    """
    if (type(N) != int) or (N <= 0):
        raise Exception("N must be a positive integer.")

    if (type(water_amount_per_unit_of_length) != float) or (
        water_amount_per_unit_of_length <= 0
    ):
        raise Exception(
            "The amount of water/length (water_amount_per_unit_of_length) must be a positive float."
        )

    if len(height) != N:
        raise Exception(
            f"The height input list has {len(height)} elements instead of {N}."
        )
    if len(left_x) != N:
        raise Exception(
            f"The left_x input list has {len(left_x)} elements instead of {N}."
        )
    if len(right_x) != N:
        raise Exception(
            f"The right_x input list has {len(right_x)} elements instead of {N}."
        )

    for i in range(N):
        if type(height[i]) != int:
            wrong_type = str(type(height[i]))
            wrong_type = wrong_type[wrong_type.find("'") + 1 : -2]
            raise Exception(
                f"The height input list has a {wrong_type} value at location {i}. The height list should only contain integer values."
            )

        if type(left_x[i]) != int:
            wrong_type = str(type(left_x[i]))
            wrong_type = wrong_type[wrong_type.find("'") + 1 : -2]
            raise Exception(
                f"The left_x input list has a {wrong_type} value at location {i}. The left_x list should only contain integer values."
            )

        if type(right_x[i]) != int:
            wrong_type = str(type(right_x[i]))
            wrong_type = wrong_type[wrong_type.find("'") + 1 : -2]
            raise Exception(
                f"The right_x input list has a {wrong_type} value at location {i}. The right_x list should only contain integer values."
            )

        if right_x[i] <= left_x[i]:
            raise Exception(
                f"The right x-coordinate of the raind drain must be greater than its left x-coordinate. At location {i} this is not verified."
            )

    # Definition of the dataframe and sorting step
    df = pd.DataFrame(
        {
            "height": height,
            "left_x": left_x,
            "right_x": right_x,
        }
    )
    df = df.sort_values(by=["height", "left_x"], ascending=[False, True])

    # Create a list with dimension equal to the wall width, where all elements are initialized to True.
    # Each time a valid rain drain is incorporated into the final input list, the corresponding list
    # entries are changed to False. This procedure ensures that subsequent rain drains cannot be placed on
    # the same positions.
    wall_width = max(right_x) - min(left_x)
    wall_availability = [True] * wall_width
    min_left_x = min(left_x)

    previous_height = min(height)
    previous_rain_drain = df.index.values[0]

    for i, drain in df.iterrows():
        left_index = int(drain["left_x"] - min_left_x)
        right_index = int(drain["right_x"] - min_left_x)

        if int(drain["height"]) < previous_height:
            wall_availability = [True] * wall_width

        outstanding_wall_availability = wall_availability[left_index:right_index]

        if set(outstanding_wall_availability) == {True}:
            wall_availability[left_index:right_index] = [False] * (
                right_index - left_index
            )
            previous_height = drain["height"]
            previous_rain_drain = i
            continue
        else:
            raise Exception(
                f"The rain drain at location {i} overlaps the rain drain at location {previous_rain_drain}."
            )


def calculate_drain_amount(
    N: int,
    height: list,
    left_x: list,
    right_x: list,
    water_amount_per_unit_of_length: float,
) -> pd.DataFrame:
    """
    Calculate drain amounts based on given parameters.

    Args:
        N (int): Number of rain drains.
        height (list): List of heights.
        left_x (list): List of left x-coordinates.
        right_x (list): List of right x-coordinates.
        water_amount_per_unit_of_length (float): Amount of water per unit of length.

    Returns:
        df: Pandas DataFrame having height, left_x, right_x and drain_amount of the rain drains as columns.
    """
    df = pd.DataFrame(
        {
            "height": height,
            "left_x": left_x,
            "right_x": right_x,
        }
    )

    # Sorting step to order the rain drains for the consequent analysis
    df = df.sort_values(by=["height", "left_x"], ascending=[False, True])

    # Initilization of the drain amount of each rain drain to zero
    df["drain_amount"] = 0.0

    # Initialization of the variables used in the loop:
    #   min_x_left: it represents the minimum left x-coordinate among the left x-coordinates of the drains
    #               Since this value might be different from zero, we need to take it into account
    #               when evaluating the indexes used to extract the sublists from "wall_rain_fall"
    #               corresponding to the rain drain under analysis.
    #   wall_with: it represents the width of the wall containing the rain drains. This value is used to
    #              define the length of the "wall_rain_fall" list.
    #   wall_rain_fall: this list has length equal to the "wall_width" and keeps track of the locations where
    #                   the drains can receive rain drops directly from the top edge of the wall and from the
    #                   right ends of the above rain drains
    min_x_left = min(left_x)
    wall_width = max(right_x) - min(left_x)
    wall_rain_fall = [water_amount_per_unit_of_length] * wall_width

    for i, drain in df.iterrows():
        left_index = int(drain["left_x"] - min_x_left)
        right_index = int(drain["right_x"] - min_x_left)

        # Extraction of the sublist of "wall_rain_fall" that corresponds to the positions above the rain drain
        # being examined
        outstanding_wall_rain_fall = wall_rain_fall[left_index:right_index]

        # Determination of the water amount falling from the right end of the examined rain drain
        # by summing the amount of water coming from the rain drops coming from the top edge of the wall
        # plus potential water amounts falling from the above rain drains
        drain_amount = sum(outstanding_wall_rain_fall)

        # Updating the "wall_rain_fall" list by setting to zero its values at the positions coinciding with
        # the rain drain under consideration, except for the entry corresponding to the position just after
        # the right end of the rain drain. This latter entry is augmented by the value of the associated drain amount.
        wall_rain_fall[left_index:right_index] = [0.0] * (right_index - left_index)
        if right_index < len(wall_rain_fall):
            wall_rain_fall[right_index] += drain_amount

        df.loc[i, "drain_amount"] = drain_amount

    # Rearranging the dataframe to match the order of the provided height, left_x, and right_x input lists.
    df = df.sort_index(ascending=True)

    return df


def generate_raindrops(
    num_drops: int,
    x_min: int,
    x_max: int,
    y_min: int,
    y_max: int,
    seed_value: int = None,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate random raindrop coordinates within specified ranges.

    Args:
        num_drops (int): Number of raindrops to generate.
        x_min (int): Minimum x-coordinate value.
        x_max (int): Maximum x-coordinate value.
        y_min (int): Minimum y-coordinate value.
        y_max (int): Maximum y-coordinate value.
        seed_value (int, optional): Seed value for random number generator. Default is None.

    Returns:
        Tuple[np.ndarray, np.ndarray]: Two NumPy arrays representing x and y coordinates of raindrops.
    """
    if seed_value is not None:
        np.random.seed(seed_value)

    # Generation of the random raindrops positions
    x = np.random.uniform(x_min, x_max, num_drops)
    y = np.random.uniform(y_min, y_max, num_drops)

    return x, y


def process_to_height_and_raindrops(
    N: int, df: pd.DataFrame, rain_drops_x: np.ndarray, rain_drops_y: np.ndarray
) -> Tuple[pd.DataFrame, np.ndarray, np.ndarray]:
    """
    Evaluating the heights of the locations where the water amounts of the different rain drains
    fall and process the raindrops based on DataFrame information.

    Args:
        N (int): Number of rain drains.
        df (pd.DataFrame): DataFrame containing height, left_x, right_x and drain amount columns.
        rain_drops_x (np.ndarray): NumPy array of raindrop x-coordinates.
        rain_drops_y (np.ndarray): NumPy array of raindrop y-coordinates.

    Returns:
        Tuple[df, np.ndarray, np.ndarray]: Updated DataFrame with to_height column and updated
                                           raindrop x-coordinates and y-coordinates NumPy arrays.
    """

    # Sorting step to order the rain drains properly
    df = df.sort_values(by=["height", "left_x"], ascending=[False, True])
    df["to_height"] = df["height"].min()

    for i in range(N):
        left_index_up = df["left_x"].iloc[i]
        right_index_up = df["right_x"].iloc[i]

        # Elimination of raindrops located beneath each rain drain upon which the raindrops fall.
        x_boolean = (rain_drops_x >= left_index_up) & (rain_drops_x <= right_index_up)
        y_boolean = rain_drops_y <= df["height"].iloc[i]
        final_boolean = ~(x_boolean & y_boolean)
        rain_drops_x = rain_drops_x[final_boolean]
        rain_drops_y = rain_drops_y[final_boolean]

        for j in range(i + 1, N):
            left_index_down = df["left_x"].iloc[j]
            right_index_down = df["right_x"].iloc[j]

            # Computing the location where the downward water stream from the right edge of the
            # rain drain stops.
            if left_index_down < right_index_up + 1 <= right_index_down:
                df.iloc[i, df.columns.get_loc("to_height")] = df.iloc[
                    j, df.columns.get_loc("height")
                ]
                break

    return df, rain_drops_x, rain_drops_y


def plot_graph(df: pd.DataFrame, rain_drops_x: np.ndarray, rain_drops_y: np.ndarray):
    """
    Plot rain drains, water falls and raindrop data.

    Args:
        df (pd.DataFrame): DataFrame containing rain drains information.
        rain_drops_x (np.ndarray): NumPy array of raindrop x-coordinates.
        rain_drops_y (np.ndarray): NumPy array of raindrop y-coordinates.
    """

    plt.figure(figsize=(10, 8))
    plt.plot(rain_drops_x, rain_drops_y, "|", c="blue", markersize=3, lw=0.5, alpha=0.3)

    for i, drain in df.iterrows():
        # Plot rain drains
        plt.plot(
            [drain["left_x"], drain["right_x"]],
            [drain["height"], drain["height"]],
            c="k",
        )
        if drain["drain_amount"] > 0:
            # Plor water streams at the right ends of the rain drains
            plt.plot(
                [drain["right_x"], drain["right_x"]],
                [drain["height"], drain["to_height"]],
                "--",
                c="blue",
            )
        # Plot drain water amounts at the right ends of the rain drains
        plt.annotate(
            f"{drain['drain_amount']:.3}",
            (drain["right_x"] * 1.02, drain["height"] * 0.98),
        )
    plt.show()