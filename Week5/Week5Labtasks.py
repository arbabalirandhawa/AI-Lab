#Task 2 
#A-Minimax

import math

minimax_count = 0

def minimax(curDepth, nodeIndex, maxTurn, scores, targetDepth):
    global minimax_count

    # Base case: targetDepth reached
    if curDepth == targetDepth:
        minimax_count += 1
        return scores[nodeIndex]

    if maxTurn:
        return max(
            minimax(curDepth + 1, nodeIndex * 2, False, scores, targetDepth),
            minimax(curDepth + 1, nodeIndex * 2 + 1, False, scores, targetDepth)
        )
    else:
        return min(
            minimax(curDepth + 1, nodeIndex * 2, True, scores, targetDepth),
            minimax(curDepth + 1, nodeIndex * 2 + 1, True, scores, targetDepth)
        )

scores = [3, 5, 2, 9, 0, 7]
treeDepth = math.ceil(math.log2(len(scores)))

scores += [0] * (2**treeDepth - len(scores))

print("Minimax optimal value:", minimax(0, 0, True, scores, treeDepth))
print("Minimax leaves evaluated:", minimax_count)

#B-Alphabeta

alphabeta_count = 0

def alphabeta(depth, index, maxTurn, scores, target, alpha, beta):
    global alphabeta_count

    if depth == target:
        alphabeta_count += 1
        return scores[index]

    if maxTurn:
        value = float('-inf')
        for i in range(2):
            value = max(value, alphabeta(depth+1, index*2+i, False, scores, target, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for i in range(2):
            value = min(value, alphabeta(depth+1, index*2+i, True, scores, target, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value


ab_scores = [3, 5, 2, 9, 3, 5, 2, 9]
depth = int(math.log2(len(ab_scores)))

print("Alpha-beta optimal value:", alphabeta(0, 0, True, ab_scores, depth, float('-inf'), float('inf')))
print("Alpha-beta leaves evaluated:", alphabeta_count)

#Task3
#A)Reordering Alpha beta

reordered_count = 0

def alphabeta_reordered(depth, index, maxTurn, scores, target, alpha, beta):
    global reordered_count

    if depth == target:
        reordered_count += 1
        return scores[index]

    if maxTurn:
        value = float('-inf')
        for i in range(2):
            value = max(value, alphabeta_reordered(depth+1, index*2+i, False, scores, target, alpha, beta))
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return value
    else:
        value = float('inf')
        for i in range(2):
            value = min(value, alphabeta_reordered(depth+1, index*2+i, True, scores, target, alpha, beta))
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value
reordered_scores = [3, 9, 0, 5, 0, 2,7,0]
depth_re = int(math.log2(len(reordered_scores)))
print("Reordered alpha-beta value:", alphabeta_reordered(0, 0, True, reordered_scores, depth_re, float('-inf'), float('inf')))
print("Reordered alpha-beta leaves evaluated:", reordered_count)


#B-Reordering MiniMax

import math

minimax_count = 0

def minimax(curDepth, nodeIndex, maxTurn, scores, targetDepth):
    global minimax_count

    # Base case: targetDepth reached
    if curDepth == targetDepth:
        minimax_count += 1
        return scores[nodeIndex]

    if maxTurn:
        return max(
            minimax(curDepth + 1, nodeIndex * 2, False, scores, targetDepth),
            minimax(curDepth + 1, nodeIndex * 2 + 1, False, scores, targetDepth)
        )
    else:
        return min(
            minimax(curDepth + 1, nodeIndex * 2, True, scores, targetDepth),
            minimax(curDepth + 1, nodeIndex * 2 + 1, True, scores, targetDepth)
        )

scores_re = [3, 9, 0, 5, 0, 2,7,0]
treeDepth = math.ceil(math.log2(len(scores_re)))

print("Reordered Minimax optimal value:", minimax(0, 0, True, scores_re, treeDepth))
print("Reordered Minimax leaves evaluated:", minimax_count)