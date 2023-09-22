import sys
import random
import itertools
import numpy as np
import cv2 as cv

MAP_FILE = 'cape_python.png'

SEARCH_AREA1_CORNERS = (130, 265, 180, 315)  # (Left Top X, Left Top Y, Right Down X, Right Down Y)
SEARCH_AREA2_CORNERS = (80, 255, 130, 305)   # (Left Top X, Left Top Y, Right Down X, Right Down Y)
SEARCH_AREA3_CORNERS = (105, 205, 155, 255)  # (Left Top X, Left Top Y, Right Down X, Right Down Y)

class Search:
    """
    A Baye's game to simulate search-rescue mission
    with three fields of search.
    """

    def __init__(self, name):
        self.name = name
        self.image = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        if self.image is None:
            print(f"Cannot load the map file {MAP_FILE}", file=sys.stderr)
            sys.exit(1)

        self.area_actual = 0
        # Local coordinates in the search area
        self.sailor_actual = [0, 0]

        self.search_area1 = self.image[SEARCH_AREA1_CORNERS[1] : SEARCH_AREA1_CORNERS[3],
                                       SEARCH_AREA1_CORNERS[0] : SEARCH_AREA1_CORNERS[2]]

        self.search_area2 = self.image[SEARCH_AREA2_CORNERS[1]: SEARCH_AREA2_CORNERS[3],
                                       SEARCH_AREA2_CORNERS[0]: SEARCH_AREA2_CORNERS[2]]

        self.search_area3 = self.image[SEARCH_AREA3_CORNERS[1]: SEARCH_AREA3_CORNERS[3],
                                       SEARCH_AREA3_CORNERS[0]: SEARCH_AREA3_CORNERS[2]]

        self.probability_area1 = 0.2
        self.probability_area2 = 0.5
        self.probability_area3 = 0.3

        self.effectiveness1 = 0
        self.effectiveness2 = 0
        self.effectiveness3 = 0

    def draw_map(self, last_known_location):
        """
        Displays the region map with a scale, the last location known
        and the searching areas.
        """
        cv.line(self.image, (20, 370), (70, 370), (0, 0, 0), 2)
        cv.putText(self.image, '0', (8, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.image, '50 sea miles', (71, 370),
                   cv.FONT_HERSHEY_PLAIN, 1, (0 ,0, 0))
        
        cv.rectangle(self.image,
                     (SEARCH_AREA1_CORNERS[0], SEARCH_AREA1_CORNERS[1]),
                     (SEARCH_AREA1_CORNERS[2], SEARCH_AREA1_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.image, '1',
                   (SEARCH_AREA1_CORNERS[0] + 3, SEARCH_AREA1_CORNERS[1] + 15),
                   cv.FONT_HERSHEY_PLAIN, 1, 0)
        cv.rectangle(self.image,
                     (SEARCH_AREA2_CORNERS[0], SEARCH_AREA2_CORNERS[1]),
                     (SEARCH_AREA2_CORNERS[2], SEARCH_AREA2_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.image, '2',
                   (SEARCH_AREA2_CORNERS[0] + 3, SEARCH_AREA2_CORNERS[1] + 15),
                   cv.FONT_HERSHEY_PLAIN, 1, 0)
        cv.rectangle(self.image,
                     (SEARCH_AREA3_CORNERS[0], SEARCH_AREA3_CORNERS[1]),
                     (SEARCH_AREA3_CORNERS[2], SEARCH_AREA3_CORNERS[3]), (0, 0 ,0), 1)
        cv.putText(self.image, '3',
                   (SEARCH_AREA3_CORNERS[0] + 3, SEARCH_AREA3_CORNERS[1] + 15),
                   cv.FONT_HERSHEY_PLAIN, 1, 0)
        
        cv.putText(self.image, '+', last_known_location, cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv.putText(self.image, '+ = last known location', (240, 355), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv.putText(self.image, '* = actual location', (240, 370), cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

        cv.imshow('Areas to be searched', self.image)
        cv.moveWindow('Areas to be searched', 750, 10)
        cv.waitKey(500)

    def sailor_final_location(self, number_of_search_areas):
        """
        Returns the x and y coordinates of the sailor's current location.
        """
        # Finds the sailor's coordinates relative to the sub-table of the search area.
        self.sailor_actual[0] = np.random.choice(self.search_area1.shape[1], 1)
        self.sailor_actual[1] = np.random.choice(self.search_area1.shape[0], 1)

        area = int(random.triangular(1, number_of_search_areas + 1))

        if area == 1:
            x = self.sailor_actual[0] + SEARCH_AREA1_CORNERS[0]
            y = self.sailor_actual[1] + SEARCH_AREA1_CORNERS[1]
            self.area_actual = 1
        elif area == 2:
            x = self.sailor_actual[0] + SEARCH_AREA2_CORNERS[0]
            y = self.sailor_actual[1] + SEARCH_AREA2_CORNERS[1]
            self.area_actual = 2
        elif area == 3:
            x = self.sailor_actual[0] + SEARCH_AREA3_CORNERS[0]
            y = self.sailor_actual[0] + SEARCH_AREA3_CORNERS[1]
            self.area_actual = 3
        return x, y

    def calculate_effectiveness(self):
        """
        Calculates a decimal value representing the effectiveness of the search for each area.
        """
        self.effectiveness1 = random.uniform(0.2, 0.9)
        self.effectiveness2 = random.uniform(0.2, 0.9)
        self.effectiveness3 = random.uniform(0.2, 0.9)

    def conduct_search(self, area_number, area_array, effectiveness_probability):
        """
        Returns the result of the search and the list of the searched coordinates.
        """
        local_y_range = range(area_array.shape[0])
        local_x_range = range(area_array.shape[1])
        coords = list(itertools.product(local_x_range, local_y_range))
        random.shuffle(coords)
        coords = coords[:int((len(coords) * effectiveness_probability))]
        location_actual = (self.sailor_actual[0], self.sailor_actual[1])
        if area_number == self.area_actual and location_actual in coords:
            return f"Found in the area number {area_number}.", coords
        else:
            return "Not found.", coords

    def revise_target_probs(self):
        """
        Updates the probability for each area based on search effectiveness.
        """
        denom = self.probability_area1 * (1 - self.effectiveness1) \
                + self.probability_area2 * (1 - self.effectiveness2) \
                + self.probability_area3 * (1 - self.effectiveness3)
        self.probability_area1 = self.probability_area1 * (1 - self.effectiveness1) / denom
        self.probability_area2 = self.probability_area2 * (1 - self.effectiveness2) / denom
        self.probability_area3 = self.probability_area3 * (1 - self.effectiveness2) / denom

def draw_menu(search_num):
    """
    Prints menu with an option to choose the area to be searched.
    """
    print(f"\nAttempt number {search_num}")
    print(
        """
        Choose the next three areas to be searched:
        
        0 - Exit the program
        1 - Search area one twice
        2 - Search area two twice
        3 - Search area three twice
        4 - Search areas one and two
        5 - Search areas one and three
        6 - Search areas two and three
        7 - Start over
        """
    )
