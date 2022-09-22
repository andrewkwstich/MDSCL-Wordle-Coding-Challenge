# MDSCL Wordle Coding Challenge June 2022

## Introduction

The code in this document was created for University of British Columbia's (UBC) Master of Data Science with Computational Linguistics (MDSCL) 2021-22 Coding Challenge, where participants were given a few hours to create a Wordle solver for English. As a bonus exercise, participants were invited to do the same for the Gitksan language, which added the challenge of simplifying the spellings of words for the purpose of collecting data about character distributions, reducing all words to 5 characters.

The Gitksan data is sourced from the UBC Department of Linguistics.

This solution was awarded second place overall, averaging around 3 guesses per word for both English and Gitksan.

## Rules of the Game

For those unfamiliar, the rules of vanilla Wordle can be found [in this blogpost](https://www.tomsguide.com/news/what-is-wordle). However, the rules are slightly harsher in the coding challenge in that a misplaced letter is still considered "yellow" even if all its other occurrences are included in the guess. For example, given the target "happy", the guess "puppy" would receive the feedback [Y, R, G, G, G].

## Description

A list of guessable words was provided for both languages. After each guess, the function `remove_words` in `instructions.ipynb` removes from the list all the words that are ruled out by the feedback to the guess.

My strategy was based on guessing, at each stage, the remaining word that maximizes this equation:

$$\sum_{i=1}^{n} p(l_{i})|pos=i$$

where $l_i$ refers to the letter at position i, and $n$ refers to the length of the word (6 letters in English, 5 in Gitksan). The word-position probabilities were determined for each language by mapping letters to a list such that each entry represents the number of occurrences of the letter at that index.

Intuitively, what the above equation does is to directly maximize the number of green letters expected for each guess. However, for the early guesses, this might not be a suitable goal: one also wants to prioritize guessing a wide variety of letters. Therefore, a multiplier was added so that early guesses are penalized for overusing the same letters. This penalty gets smaller with each subsequent guess and is absent after the third guess. The final form of the equation to be maximized is then as follows:

$$\sum_{i=1}^{n} \begin{Bmatrix}
(p(l_{i})|pos=i) \times min(\frac{g}{4},1), \quad l_i \text{already attempted}
\\ 
p(l_{i})|pos=i, \qquad \qquad \qquad \quad l_i \text{not yet attempted}
\end{Bmatrix}$$

where $g$ is the number of preceding guesses, and "attempted" refers to whether the letter has been guessed at any point for this word. Adding this penalty was found to reduce the number of guesses required.

## How to Run the Code

Instructions for the coding challenge, along with code to evaluate submissions, are found in `instructions.ipynb`. Most of this document was created by the coding challenge organizers; see the file for details.

The English and Gitksan solutions are both found in `solution.ipynb`, along with a few tests to ensure that the functions work as intended.

## Requirements

This submission was created in Python 3.9. It does not depend on any external libraries.
