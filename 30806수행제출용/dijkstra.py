import heapq


def dijkstra(graph, start, end):

    queue = [(0, start, [])]

    visited = set()

    while queue:

        cost, node, path = heapq.heappop(queue)

        if node in visited:
            continue

        visited.add(node)

        path = path + [node]

        # 도착
        if node == end:
            return cost, path

        # 연결 노드 탐색
        neighbors = graph.get(node, [])

        for next_node, weight in neighbors:

            if next_node not in visited:

                heapq.heappush(
                    queue,
                    (
                        cost + weight,
                        next_node,
                        path
                    )
                )

    return float("inf"), []