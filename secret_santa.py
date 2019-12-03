import random
from typing import List

from graphviz import Digraph

from Person import Person


def gift_ok(p1: Person, p2: Person, forbidden_pairs=None) -> bool:
    if p1 == p2:
        return False
    if p1.spouse == p2:
        return False
    if p2 in p1.parents or p1 in p2.parents:
        return False
    for parent in p1.parents:
        if parent in p2.parents:
            return False
    if forbidden_pairs:
        for fp in forbidden_pairs:
            if p1.name == fp[0] and p2.name == fp[1]:
                return False
    return True


def generate(people: List[Person], name, forbidden_pairs=None):
    ungifted = people.copy()
    random.shuffle(ungifted)
    gifted = [ungifted.pop()]

    dot = Digraph("Richerd", format="png", engine="neato")

    while ungifted:
        found = False
        for i in range(len(ungifted)):
            if gift_ok(gifted[-1], ungifted[i], forbidden_pairs):
                person = ungifted.pop(i)
                gifted.append(person)
                # print(person.name)
                found = True
                break
        if not found:
            print("sorry, I failed :c")
            return

    for i in range(-1, len(gifted) - 1):
        dot.edge(gifted[i].name, gifted[i + 1].name)
    # for i in range(len(ungifted) - 1):
    #     for j in range(i + 1, len(ungifted)):
    #         if gift_ok(ungifted[i], ungifted[j]):
    #             print(ungifted[i].name, '=>', ungifted[j].name)
    #             dot.edge(ungifted[i].name, ungifted[j].name)
    #             break

    # print("ungifted :", ungifted)
    # print(gifted)
    dot.render(f"tmp/{name}.gv", view=True)


if __name__ == '__main__':
    people = Person.from_csv("data/people.csv", "data/children.csv", "data/spouses.csv")
    generate(list(people.values()), f"Richerd_santa", [('Laurent', 'Joël')])
