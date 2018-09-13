import sys
import collections

def main():
    clauses = storeClauses(open(sys.argv[1]))
    returned = applyResolution(clauses)
    if returned  == []:
        print("Failure")
        print("Size of final clause set: ", len(clauses))
        exit(0)

    else:
        clauses = returned
        path = getProofPath(clauses)
        for clause in path:
            literalString = " ".join(str(l) for l in clause.literals)
            parentString = "{" + ",".join(str(p) for p in clause.parents) + "}"
            print((clauses.index(clause) + 1) , "." , literalString + "\t", parentString)
        print("Size of final clause set: ", len(clauses))

def storeClauses(file):
    clauses = []
    i = 1
    for line in file:
        if line[-1] == '\n':
            clauses.append(Clause(line[:-1].split(" ")))
        else:
            clauses.append(Clause(line.split(" ")))
        i += 1
    return clauses

def shortestLength(startIndex,endPoint,clauses):
    min = 10000000
    i = startIndex
    while i < endPoint:
        if len(clauses[i].literals) < min:
            min = len(clauses[i].literals)
        i += 1
    return min

def checkUnique(lst ,clauses):
    for clause in clauses:
        if ((len(lst) == len(clause.literals)) and
                (all(i in clause.literals for i in lst))):
            return False
    return True

def multipleResolvableLiterals(clause1,clause2):
    oneResolvablePair = False
    for literal in clause1.literals:
        if "~" + literal in clause2.literals:
            if oneResolvablePair:
                return True
            else:
                oneResolvablePair = True
        elif "~" in literal and literal.replace("~","") in clause2.literals:
            if oneResolvablePair:
                    return True
            else:
                oneResolvablePair = True
    return False

def removeDupeLiterals(literals):
    i = len(literals) - 1
    for literal in literals:
        while literals.count(literals[i]) > 1:
            literals.remove(literals[i])
            i -= 1
        i -= 1

    return literals


def applyResolution(clauses):
    hasNilClause = False
    outOfResolutions = False
    firstClauseToSearch = 0

    while not outOfResolutions and not hasNilClause:
        outOfResolutions = True
        nextFirstClause = len(clauses)

        currentLength = shortestLength(firstClauseToSearch, nextFirstClause, clauses)
        clausesChecked = 0
        while clausesChecked < nextFirstClause - firstClauseToSearch and not hasNilClause:
            i = firstClauseToSearch
            while i < nextFirstClause and not hasNilClause:

                if len(clauses[i].literals) == currentLength:
                    clausesChecked += 1
                    j = i - 1

                    while j >= 0 and not hasNilClause:
                        if multipleResolvableLiterals(clauses[i],clauses[j]):
                            j -= 1
                            continue
                        for literal in clauses[i].literals:
                            if "~" + literal in clauses[j].literals:
                                if len(clauses[i].literals) == 1 and len(clauses[j].literals) == 1:

                                    clauses.append(Clause(["False"], [i + 1, j + 1]))
                                    hasNilClause = True
                                    break
                                else:
                                    newLiterals = clauses[i].literals + clauses[j].literals
                                    newLiterals.remove(literal)
                                    newLiterals.remove("~" + literal)
                                    newLiterals = removeDupeLiterals(newLiterals)
                                    if checkUnique(newLiterals, clauses):
                                        clauses.append(Clause(newLiterals, [i + 1, j + 1]))
                                        outOfResolutions = False
                                        break
                            elif "~" in literal and literal.replace("~", "") in clauses[j].literals:
                                if len(clauses[i].literals) == 1 and len(clauses[j].literals) == 1:
                                    clauses.append(Clause(["False"], [i + 1, j + 1]))
                                    hasNilClause = True
                                    break
                                else:
                                    newLiterals = clauses[i].literals + clauses[j].literals
                                    newLiterals.remove(literal)
                                    newLiterals.remove(literal.replace("~", ""))
                                    newLiterals = removeDupeLiterals(newLiterals)
                                    if checkUnique(newLiterals, clauses):
                                        clauses.append(Clause(newLiterals, [i + 1, j + 1]))
                                        outOfResolutions = False
                                        break
                        j -= 1
                i += 1
            else:
                currentLength += 1

        firstClauseToSearch = nextFirstClause


    if not hasNilClause: #exited loop without nil clause
        return []
    else:
        return clauses


def getProofPath(clauses):
    path = []
    for clause in clauses:
        if clause.literals == ["False"]:
            nilIndex = clauses.index(clause)
            break

    path.append(clauses[nilIndex])
    i = 0
    while i < len(path):
        currentClause = path[i]

        for parentIndex in currentClause.parents:
            if clauses[parentIndex - 1] in path:
                continue
            path.append(clauses[parentIndex - 1])
        i += 1

    path = sorted(path, key=clauses.index)

    return path

class Clause (object):
    def __init__(self, lits, parents = []):
        self.literals = lits
        self.parents = parents

main()

