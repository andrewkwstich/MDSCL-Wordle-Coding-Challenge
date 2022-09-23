# MDSCL Wordle Coding Challenge June 2022

## Introduction

The code in this repository was originally submitted as an entry for University of British Columbia's (UBC) Master of Data Science with Computational Linguistics (MDSCL) 2021-22 Coding Challenge, where participants were given a few hours to create a Wordle solver for English. As a bonus exercise, participants were invited to do the same for the Gitksan language, which added the challenge of simplifying the spellings of words for the purpose of collecting data about character distributions, reducing all words to 5 characters.

As the Gitksan data for the challenge was sourced from the UBC Department of Linguistics, it is available by request only.

This solution was awarded second place overall, averaging around 3 guesses per word for both English and Gitksan.

## Rules of the Game

For those unfamiliar, the rules of vanilla Wordle can be found [in this blogpost](https://www.tomsguide.com/news/what-is-wordle). However, the rules are slightly harsher in the coding challenge version in that a misplaced letter is still considered "yellow" even if all its other occurrences are included in the guess. For example, given the target "happy", the guess "puppy" would receive the feedback [Y, R, G, G, G].

## Description

### Wordle Solution

A list of guessable words was provided for both languages. After each guess, the function `remove_words` in `instructions.ipynb` removes from the list all the words that are ruled out by the feedback to the guess (outputted by the provided function `getFeedback`).

My strategy was based on guessing, at each stage, the word in the remaining domain that maximizes the below sum:

$$guess = argmax(\sum_{i=1}^{n} P(l_{wi})|pos=i)$$

where $l_wi$ refers to the letter in word w at position i, $n$ refers to the length of the word (6 letters in English, 5 in Gitksan), and $pos$ refers to the position of $l_wi$ in the word. The probabilities of letters conditional on position were represented for each language by mapping letters to a list such that each list entry represents the number of occurrences of the letter at that index across all words in the word-list.

Intuitively, what this amounts to is to directly maximize the number of green letters expected for each guess. However, for the early guesses, this might not be a suitable goal: one also wants to prioritize guessing a wide variety of letters. Therefore, a multiplier was added so that early guesses are penalized for overusing the same letters. This penalty gets smaller with each subsequent guess and is absent after the third guess. The final form of the sum to be maximized is then as follows:

guess = argmax\left (\sum_{i=1}^{n} \begin{Bmatrix}
(P(l_{wi})|pos=i) \times min(\frac{g}{4},1), \quad l_i \text{ already attempted}
\\ 
P(l_{wi})|pos=i, \qquad \qquad \qquad \quad l_i \text{ not yet attempted}
\end{Bmatrix} \right )

where $g$ is the number of preceding guesses, and "attempted" refers to whether the letter has been guessed at any point for this word. Adding this penalty was found to reduce the number of guesses required.

### Gitksan Encoding

Gitksan words were encoded so that each multigraph (e.g., "k_'") was encoded as a single arbitrary character. This was accomplished using a concatenation of string manipulation rules. A rule is triggered if the current character belongs to a particular (linguistically inspired) domain (e.g. "vowels"), which helped minimize the number of rules needed.

## How to Run the Code

Instructions for the coding challenge, along with code to evaluate submissions, are found in `instructions.ipynb`. Most of the notebook was created by the coding challenge organizers; see `instructions.ipynb` for details.

To see the results, simply run `instructions.ipynb`. If you do not have access to the Gitksan data, comment out the code under "Task 2".

The English and Gitksan solutions are both found in `solution.ipynb`, along with a few tests to ensure that the functions work as intended.

### Requirements

This submission was created in Python 3.9. It does not depend on any external libraries.
