from pprint import pprint
from typing import List, Dict, Optional
import csv

from graphviz import Digraph


class Person:
    def __init__(self, name: str) -> None:
        self.name = name
        self.parents: List[Person] = []
        self.children: List[Person] = []
        self.spouse: Optional[Person] = None

    def add_child(self, p: 'Person') -> None:
        self.children.append(p)
        p.parents.append(self)

    def add_spouse(self, p: 'Person') -> None:
        self.spouse = p
        p.spouse = self

    def __repr__(self) -> str:
        if not self.parents:
            return self.name
        elif len(self.parents) == 1:
            return f"{self.name} , child of {self.parents[0]}"
        return f"{self.name} , child of {self.parents}"

    def graph(self, graph: Digraph) -> None:
        graph.node(self.name, )
        for p in self.children:
            p.graph(graph)
            graph.edge(self.name, p.name)
        if self.spouse and self.name < self.spouse.name:
            with graph.subgraph(name=f"cluster{self.name}-{self.spouse.name}") as subgraph:
                subgraph.attr(rank="same", style="dotted", color="white")
                subgraph.node(self.name)
                subgraph.node(self.spouse.name)
                subgraph.edge(self.name, self.spouse.name, constraint="false", arrowhead="none")

    def generation(self) -> int:
        if not self.parents:
            return 0
        return min([p.generation() for p in self.parents])

    @staticmethod
    def from_csv(people_filename: str, children_filename: str, spouses_filename: str) -> Dict[str, 'Person']:
        people = {}
        with open(people_filename, 'r') as f1, \
                open(children_filename, 'r') as f2, \
                open(spouses_filename, 'r') as f3:
            people_csv = csv.reader(f1)
            children_csv = csv.reader(f2)
            spouse_csv = csv.reader(f3)

            # skip headers
            next(people_csv)
            next(children_csv)
            next(spouse_csv)

            for line in people_csv:
                name = line[0]
                people[name] = Person(name)

            for parent_name, child_name in children_csv:
                people[parent_name].add_child(people[child_name])

            for spouse1, spouse2 in spouse_csv:
                people[spouse1].add_spouse(people[spouse2])

        # pprint(people)
        return people


if __name__ == '__main__':
    dot = Digraph("Richerd", format="png")
    # dot.attr()
    for p in Person.from_csv("data/people.csv", "data/children.csv", "data/spouses.csv").values():
        if not p.parents:
            p.graph(dot)
    pprint(dot.source)
    dot.render("tmp/richerd.gv", view=True)
