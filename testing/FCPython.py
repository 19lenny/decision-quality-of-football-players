#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:32:00 2020

@author: davsu428
"""
import matplotlib.pyplot as plt
from matplotlib.patches import Arc


def createPitch(length, width, unity, linecolor):  # in meters
    # Code by @JPJ_dejong

    """
    creates a plot in which the 'length' is the length of the pitch (goal to goal).
    And 'width' is the width of the pitch (sideline to sideline).
    Fill in the unity in meters or in yards.

    """
    # Set unity
    if unity == "meters":
        # Set boundaries
        if length >= 120.5 or width >= 75.5:
            return (str("Field dimensions are too big for meters as unity, didn't you mean yards as unity?\
                       Otherwise the maximum length is 120 meters and the maximum width is 75 meters. Please try again"))
        # Run program if unity and boundaries are accepted
        else:
            # Create figure
            fig = plt.figure()
            # fig.set_size_inches(7, 5)
            ax = fig.add_subplot(1, 1, 1)

            # Pitch Outline & Centre Line
            plt.plot([0, 0], [0, width], color=linecolor)
            plt.plot([0, length], [width, width], color=linecolor)
            plt.plot([length, length], [width, 0], color=linecolor)
            plt.plot([length, 0], [0, 0], color=linecolor)
            plt.plot([length / 2, length / 2], [0, width], color=linecolor)

            # Left Penalty Area
            plt.plot([16.5, 16.5], [(width / 2 + 16.5), (width / 2 - 16.5)], color=linecolor)
            plt.plot([0, 16.5], [(width / 2 + 16.5), (width / 2 + 16.5)], color=linecolor)
            plt.plot([16.5, 0], [(width / 2 - 16.5), (width / 2 - 16.5)], color=linecolor)

            # Right Penalty Area
            plt.plot([(length - 16.5), length], [(width / 2 + 16.5), (width / 2 + 16.5)], color=linecolor)
            plt.plot([(length - 16.5), (length - 16.5)], [(width / 2 + 16.5), (width / 2 - 16.5)], color=linecolor)
            plt.plot([(length - 16.5), length], [(width / 2 - 16.5), (width / 2 - 16.5)], color=linecolor)

            # Left 5-meters Box
            plt.plot([0, 5.5], [(width / 2 + 7.32 / 2 + 5.5), (width / 2 + 7.32 / 2 + 5.5)], color=linecolor)
            plt.plot([5.5, 5.5], [(width / 2 + 7.32 / 2 + 5.5), (width / 2 - 7.32 / 2 - 5.5)], color=linecolor)
            plt.plot([5.5, 0.5], [(width / 2 - 7.32 / 2 - 5.5), (width / 2 - 7.32 / 2 - 5.5)], color=linecolor)

            # Right 5 -eters Box
            plt.plot([length, length - 5.5], [(width / 2 + 7.32 / 2 + 5.5), (width / 2 + 7.32 / 2 + 5.5)],
                     color=linecolor)
            plt.plot([length - 5.5, length - 5.5], [(width / 2 + 7.32 / 2 + 5.5), width / 2 - 7.32 / 2 - 5.5],
                     color=linecolor)
            plt.plot([length - 5.5, length], [width / 2 - 7.32 / 2 - 5.5, width / 2 - 7.32 / 2 - 5.5], color=linecolor)

            # Prepare Circles
            centreCircle = plt.Circle((length / 2, width / 2), 9.15, color=linecolor, fill=False)
            centreSpot = plt.Circle((length / 2, width / 2), 0.8, color=linecolor)
            leftPenSpot = plt.Circle((11, width / 2), 0.8, color=linecolor)
            rightPenSpot = plt.Circle((length - 11, width / 2), 0.8, color=linecolor)

            # Draw Circles
            ax.add_patch(centreCircle)
            ax.add_patch(centreSpot)
            ax.add_patch(leftPenSpot)
            ax.add_patch(rightPenSpot)

            # Prepare Arcs
            leftArc = Arc((11, width / 2), height=18.3, width=18.3, angle=0, theta1=308, theta2=52, color=linecolor)
            rightArc = Arc((length - 11, width / 2), height=18.3, width=18.3, angle=0, theta1=128, theta2=232,
                           color=linecolor)

            # Draw Arcs
            ax.add_patch(leftArc)
            ax.add_patch(rightArc)
            # Axis titles

    # check unity again
    elif unity == "yards":
        # check boundaries again
        if length <= 95:
            return (str("Didn't you mean meters as unity?"))
        elif length >= 131 or width >= 101:
            return (str("Field dimensions are too big. Maximum length is 130, maximum width is 100"))
        # Run program if unity and boundaries are accepted
        else:
            # Create figure
            fig = plt.figure()
            # fig.set_size_inches(7, 5)
            ax = fig.add_subplot(1, 1, 1)

            # Pitch Outline & Centre Line
            plt.plot([0, 0], [0, width], color=linecolor)
            plt.plot([0, length], [width, width], color=linecolor)
            plt.plot([length, length], [width, 0], color=linecolor)
            plt.plot([length, 0], [0, 0], color=linecolor)
            plt.plot([length / 2, length / 2], [0, width], color=linecolor)

            # Left Penalty Area
            plt.plot([18, 18], [(width / 2 + 18), (width / 2 - 18)], color=linecolor)
            plt.plot([0, 18], [(width / 2 + 18), (width / 2 + 18)], color=linecolor)
            plt.plot([18, 0], [(width / 2 - 18), (width / 2 - 18)], color=linecolor)

            # Right Penalty Area
            plt.plot([(length - 18), length], [(width / 2 + 18), (width / 2 + 18)], color=linecolor)
            plt.plot([(length - 18), (length - 18)], [(width / 2 + 18), (width / 2 - 18)], color=linecolor)
            plt.plot([(length - 18), length], [(width / 2 - 18), (width / 2 - 18)], color=linecolor)

            # Left 6-yard Box
            plt.plot([0, 6], [(width / 2 + 7.32 / 2 + 6), (width / 2 + 7.32 / 2 + 6)], color=linecolor)
            plt.plot([6, 6], [(width / 2 + 7.32 / 2 + 6), (width / 2 - 7.32 / 2 - 6)], color=linecolor)
            plt.plot([6, 0], [(width / 2 - 7.32 / 2 - 6), (width / 2 - 7.32 / 2 - 6)], color=linecolor)

            # Right 6-yard Box
            plt.plot([length, length - 6], [(width / 2 + 7.32 / 2 + 6), (width / 2 + 7.32 / 2 + 6)], color=linecolor)
            plt.plot([length - 6, length - 6], [(width / 2 + 7.32 / 2 + 6), width / 2 - 7.32 / 2 - 6], color=linecolor)
            plt.plot([length - 6, length], [(width / 2 - 7.32 / 2 - 6), width / 2 - 7.32 / 2 - 6], color=linecolor)

            # Prepare Circles; 10 yards distance. penalty on 12 yards
            centreCircle = plt.Circle((length / 2, width / 2), 10, color=linecolor, fill=False)
            centreSpot = plt.Circle((length / 2, width / 2), 0.8, color=linecolor)
            leftPenSpot = plt.Circle((12, width / 2), 0.8, color=linecolor)
            rightPenSpot = plt.Circle((length - 12, width / 2), 0.8, color=linecolor)

            # Draw Circles
            ax.add_patch(centreCircle)
            ax.add_patch(centreSpot)
            ax.add_patch(leftPenSpot)
            ax.add_patch(rightPenSpot)

            # Prepare Arcs
            leftArc = Arc((11, width / 2), height=20, width=20, angle=0, theta1=312, theta2=48, color=linecolor)
            rightArc = Arc((length - 11, width / 2), height=20, width=20, angle=0, theta1=130, theta2=230,
                           color=linecolor)

            # Draw Arcs
            ax.add_patch(leftArc)
            ax.add_patch(rightArc)

    # Tidy Axes
    plt.axis('off')

    return fig, ax


def createPitchOld(linecolor=None):
    # Taken from FC Python
    # Create figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    

    # Pitch Outline & Centre Line
    # this drasw the outer line of the pitch
    # the first list is the x coordinates
    #the second one the y coordinated
    plt.plot([0, 0], [0, 80], color=linecolor)
    plt.plot([0, 120], [80, 80], color=linecolor)
    plt.plot([120, 120], [80, 0], color=linecolor)
    plt.plot([120, 0], [0, 0], color=linecolor)
    plt.plot([60, 60], [0, 80], color=linecolor)

    # Left Penalty Area
    plt.plot([0, 18], [18, 18], color=linecolor)
    plt.plot([18, 18], [62, 18], color=linecolor)
    plt.plot([0, 18], [62, 62], color=linecolor)

    # Right Penalty Area
    plt.plot([120, 102], [18, 18], color=linecolor)
    plt.plot([102, 102], [62, 18], color=linecolor)
    plt.plot([102, 120], [62, 62], color=linecolor)

    # Left 6-yard Box
    plt.plot([0, 6], [30, 30], color=linecolor)
    plt.plot([6, 6], [50, 30], color=linecolor)
    plt.plot([6, 0], [50, 50], color=linecolor)

    # Right 6-yard Box
    plt.plot([120, 114], [30, 30], color=linecolor)
    plt.plot([114, 114], [50, 30], color=linecolor)
    plt.plot([114, 120], [50, 50], color=linecolor)

    # Prepare Circles
    centreCircle = plt.Circle((50, 40), 9.15, color=linecolor, fill=False)
    centreSpot = plt.Circle((50, 40), 0.8, color=linecolor)
    leftPenSpot = plt.Circle((12, 40), 0.8, color=linecolor)
    rightPenSpot = plt.Circle((108, 40), 0.8, color=linecolor)

    # Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    # Prepare Arcs
    leftArc = Arc((18, 40), height=18.3, width=18.3, angle=0, theta1=310, theta2=50, color=linecolor)
    rightArc = Arc((102, 40), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color=linecolor)

    # Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

    # Tidy Axes
    plt.axis('off')

    return fig, ax


def createGoalMouth():
    # Adopted from FC Python
    # Create figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    linecolor = 'white'

    # Pitch Outline & Centre Line
    plt.plot([60, 120], [0, 0], color=linecolor)
    plt.plot([60, 60], [80, 0], color=linecolor)
    plt.plot([60, 120], [80, 80], color=linecolor)

    # Right Penalty Area
    plt.plot([102, 120], [18, 18], color=linecolor)
    plt.plot([102, 102], [18, 62], color=linecolor)
    plt.plot([102, 120], [62, 62], color=linecolor)

    # Right 6-yard Box
    plt.plot([114, 120], [30, 30], color=linecolor)
    plt.plot([114, 114], [30, 50], color=linecolor)
    plt.plot([114, 120], [50, 50], color=linecolor)

    # Right Goal
    plt.plot([122, 122], [36, 44], color=linecolor)
    plt.plot([120, 122], [36, 36], color=linecolor)
    plt.plot([120, 122], [44, 44], color=linecolor)

    # Prepare Circles
    centreCircle = plt.Circle((50, 40), 9.15, color=linecolor, fill=False)
    centreSpot = plt.Circle((50, 40), 0.8, color=linecolor)

    rightPenSpot = plt.Circle((108, 40), 0.8, color=linecolor)

    # Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(rightPenSpot)

    # Prepare Arcs

    rightArc = Arc((102, 40), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color=linecolor)

    # Draw Arcs

    ax.add_patch(rightArc)

    # Tidy Axes
    plt.axis('off')

    return fig, ax

