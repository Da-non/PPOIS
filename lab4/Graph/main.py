"""
@file main_graph.py
@brief Главный файл, демонстрирующий функциональность направленного графа
@details Этот файл содержит примеры использования класса DirectedGraph
         с различными операциями и вариантами использования.
"""

from graph import DirectedGraph
from typing import List


class City:
    """
    @brief Пользовательский класс, представляющий город (для демонстрации графов с пользовательскими типами)
    """
    
    def __init__(self, name: str, population: int):
        """
        @brief Конструктор для City
        @param name Название города
        @param population Население города
        """
        self.name = name
        self.population = population
    
    def __str__(self):
        """@brief Строковое представление"""
        return f"{self.name}({self.population})"
    
    def __repr__(self):
        """@brief Repr для отладки"""
        return f"City('{self.name}', {self.population})"
    
    def __eq__(self, other):
        """@brief Сравнение на равенство"""
        if not isinstance(other, City):
            return False
        return self.name == other.name and self.population == other.population
    
    def __hash__(self):
        """@brief Хеш для использования в множествах/словарях"""
        return hash((self.name, self.population))
    
    def __lt__(self, other):
        """@brief Сравнение "меньше чем" (для сортировки)"""
        return self.name < other.name


def demo_basic_operations():
    """
    @brief Demonstrates basic graph operations
    """
    print("=" * 70)
    print("БАЗОВЫЕ ОПЕРАЦИИ С ГРАФОМ")
    print("=" * 70)
    
    graph = DirectedGraph[str]()
    
    # Adding vertices
    print("\n1. Добавление вершин:")
    vertices = ["A", "B", "C", "D", "E"]
    for v in vertices:
        result = graph.add_vertex(v)
        print(f"   Добавлена вершина '{v}': {result}")
    
    # Try adding duplicate
    print(f"   Добавление дублирующей вершины 'A': {graph.add_vertex('A')}")
    
    # Adding edges
    print("\n2. Добавление рёбер:")
    edges = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("E", "A")]
    for src, tgt in edges:
        result = graph.add_edge(src, tgt)
        print(f"   Добавлено ребро {src} -> {tgt}: {result}")
    
    # Try adding duplicate edge
    print(f"   Добавление дублирующего ребра A -> B: {graph.add_edge('A', 'B')}")
    
    # Display graph
    print("\n3. Текущая структура графа:")
    print(graph)
    
    # Check vertices and edges
    print("4. Проверка вершин и рёбер:")
    print(f"   Есть вершина 'A': {graph.has_vertex('A')}")
    print(f"   Есть вершина 'Z': {graph.has_vertex('Z')}")
    print(f"   Есть ребро A -> B: {graph.has_edge('A', 'B')}")
    print(f"   Есть ребро B -> A: {graph.has_edge('B', 'A')}")
    
    # Counts
    print("\n5. Статистика графа:")
    print(f"   Всего вершин: {graph.vertex_count()}")
    print(f"   Всего рёбер: {graph.edge_count()}")
    print(f"   Пуст: {graph.is_empty()}")


def demo_degree_calculations():
    """
    @brief Demonstrates degree calculations
    """
    print("\n" + "=" * 70)
    print("ВЫЧИСЛЕНИЕ СТЕПЕНЕЙ")
    print("=" * 70)
    
    graph = DirectedGraph[str]()
    
    # Create a sample graph
    vertices = ["A", "B", "C", "D"]
    for v in vertices:
        graph.add_vertex(v)
    
    edges = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "D"), ("D", "A"), ("D", "B")]
    for src, tgt in edges:
        graph.add_edge(src, tgt)
    
    print("\nСтруктура графа:")
    print(graph)
    
    print("Анализ степеней:")
    for vertex in sorted(vertices):
        out_deg = graph.out_degree(vertex)
        in_deg = graph.in_degree(vertex)
        total_deg = graph.degree(vertex)
        print(f"   Vertex '{vertex}':")
        print(f"      Исходящая степень: {out_deg}")
        print(f"      Входящая степень:  {in_deg}")
        print(f"      Всего:      {total_deg}")


def demo_iterators():
    """
    @brief Demonstrates various iterators
    """
    print("\n" + "=" * 70)
    print("ДЕМОНСТРАЦИЯ ИТЕРАТОРОВ")
    print("=" * 70)
    
    graph = DirectedGraph[str]()
    
    # Build graph
    vertices = ["A", "B", "C", "D"]
    for v in vertices:
        graph.add_vertex(v)
    
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "A")]
    for src, tgt in edges:
        graph.add_edge(src, tgt)
    
    print("\n1. Итерация по всем вершинам:")
    print("   ", end="")
    for vertex in graph.vertices():
        print(vertex, end=" ")
    print()
    
    print("\n2. Итерация по всем рёбрам:")
    for src, tgt in graph.edges():
        print(f"   {src} -> {tgt}")
    
    print("\n3. Смежные вершины для каждой вершины:")
    for vertex in sorted(graph.vertices(), key=str):
        adj = list(graph.adjacent_vertices(vertex))
        print(f"   Смежные с '{vertex}': {sorted(adj, key=str)}")
    
    print("\n4. Инцидентные рёбра для вершины 'D':")
    for src, tgt in graph.incident_edges("D"):
        print(f"   {src} -> {tgt}")
    
    print("\n5. Исходящие рёбра из vertex 'A':")
    for src, tgt in graph.outgoing_edges("A"):
        print(f"   {src} -> {tgt}")
    
    print("\n6. Входящие рёбра в vertex 'D':")
    for src, tgt in graph.incoming_edges("D"):
        print(f"   {src} -> {tgt}")


def demo_removal_operations():
    """
    @brief Demonstrates vertex and edge removal
    """
    print("\n" + "=" * 70)
    print("ОПЕРАЦИИ УДАЛЕНИЯ")
    print("=" * 70)
    
    graph = DirectedGraph[str]()
    
    # Build graph
    vertices = ["A", "B", "C", "D", "E"]
    for v in vertices:
        graph.add_vertex(v)
    
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("E", "A")]
    for src, tgt in edges:
        graph.add_edge(src, tgt)
    
    print("\nInitial graph:")
    print(graph)
    
    # Remove edge
    print("1. Removing edge A -> B:")
    result = graph.remove_edge("A", "B")
    print(f"   Result: {result}")
    print(f"   Edge count: {graph.edge_count()}")
    
    # Try removing non-existent edge
    print("\n2. Removing non-existent edge A -> B again:")
    result = graph.remove_edge("A", "B")
    print(f"   Result: {result}")
    
    # Remove vertex
    print("\n3. Removing vertex 'D' (will remove all its edges):")
    print(f"   Before: {graph.edge_count()} edges")
    result = graph.remove_vertex("D")
    print(f"   Result: {result}")
    print(f"   After: {graph.edge_count()} edges")
    print(f"   Vertex count: {graph.vertex_count()}")
    
    print("\n4. Graph after removals:")
    print(graph)
    
    # Clear graph
    print("5. Clearing entire graph:")
    graph.clear()
    print(f"   Vertices: {graph.vertex_count()}")
    print(f"   Edges: {graph.edge_count()}")
    print(f"   Пуст: {graph.is_empty()}")


def demo_custom_type():
    """
    @brief Demonstrates graph with custom City type
    """
    print("\n" + "=" * 70)
    print("GRAPH WITH CUSTOM TYPE (City)")
    print("=" * 70)
    
    graph = DirectedGraph[City]()
    
    # Create cities
    cities = [
        City("New York", 8_000_000),
        City("Los Angeles", 4_000_000),
        City("Chicago", 2_700_000),
        City("Houston", 2_300_000),
        City("Phoenix", 1_700_000)
    ]
    
    print("\n1. Adding cities as vertices:")
    for city in cities:
        graph.add_vertex(city)
        print(f"   Added: {city}")
    
    # Add connections (flight routes)
    print("\n2. Adding flight routes (edges):")
    routes = [
        (cities[0], cities[1]),  # NY -> LA
        (cities[0], cities[2]),  # NY -> Chicago
        (cities[1], cities[3]),  # LA -> Houston
        (cities[2], cities[3]),  # Chicago -> Houston
        (cities[3], cities[4]),  # Houston -> Phoenix
        (cities[4], cities[0]),  # Phoenix -> NY
    ]
    
    for src, tgt in routes:
        graph.add_edge(src, tgt)
        print(f"   {src.name} -> {tgt.name}")
    
    print("\n3. Статистика графа:")
    print(f"   Cities: {graph.vertex_count()}")
    print(f"   Routes: {graph.edge_count()}")
    
    print("\n4. Analyzing New York:")
    ny = cities[0]
    print(f"   Outgoing flights: {graph.out_degree(ny)}")
    print(f"   Incoming flights: {graph.in_degree(ny)}")
    print(f"   Direct destinations from New York:")
    for dest in graph.adjacent_vertices(ny):
        print(f"      - {dest.name}")


def demo_graph_algorithms():
    """
    @brief Demonstrates basic graph algorithms
    """
    print("\n" + "=" * 70)
    print("АЛГОРИТМЫ НА ГРАФАХ")
    print("=" * 70)
    
    graph = DirectedGraph[str]()
    
    # Build graph
    vertices = ["A", "B", "C", "D", "E", "F"]
    for v in vertices:
        graph.add_vertex(v)
    
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("D", "E"), ("E", "F"), ("F", "A")]
    for src, tgt in edges:
        graph.add_edge(src, tgt)
    
    print("\nGraph for algorithms:")
    print(graph)
    
    # Simple path finding (BFS-based)
    def has_path(graph: DirectedGraph[str], start: str, end: str) -> bool:
        """Check if there's a path from start to end"""
        if not graph.has_vertex(start) or not graph.has_vertex(end):
            return False
        
        visited = set()
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            if current == end:
                return True
            
            if current in visited:
                continue
            
            visited.add(current)
            for neighbor in graph.adjacent_vertices(current):
                if neighbor not in visited:
                    queue.append(neighbor)
        
        return False
    
    print("1. Path existence (BFS):")
    test_paths = [("A", "F"), ("F", "E"), ("B", "A"), ("D", "C")]
    for src, tgt in test_paths:
        exists = has_path(graph, src, tgt)
        print(f"   Path from {src} to {tgt}: {exists}")
    
    # Detect cycle
    def has_cycle(graph: DirectedGraph[str]) -> bool:
        """Detect if graph has a cycle"""
        visited = set()
        rec_stack = set()
        
        def visit(vertex: str) -> bool:
            visited.add(vertex)
            rec_stack.add(vertex)
            
            for neighbor in graph.adjacent_vertices(vertex):
                if neighbor not in visited:
                    if visit(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            
            rec_stack.remove(vertex)
            return False
        
        for vertex in graph.vertices():
            if vertex not in visited:
                if visit(vertex):
                    return True
        
        return False
    
    print("\n2. Cycle detection:")
    print(f"   Graph has cycle: {has_cycle(graph)}")


def main():
    """
    @brief Main function to run all demonstrations
    """
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "ДЕМОНСТРАЦИЯ НАПРАВЛЕННОГО ГРАФА" + " " * 25 + "║")
    print("║" + " " * 12 + "Variant 6: Adjacency List Representation" + " " * 16 + "║")
    print("╚" + "=" * 68 + "╝")
    
    demo_basic_operations()
    demo_degree_calculations()
    demo_iterators()
    demo_removal_operations()
    demo_custom_type()
    demo_graph_algorithms()
    
    print("\n" + "=" * 70)
    print("Все демонстрации успешно завершены!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
