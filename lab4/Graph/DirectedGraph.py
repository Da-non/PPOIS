from typing import TypeVar, Generic, Dict, List, Set, Tuple, Optional, Iterator
from collections import defaultdict

T = TypeVar('T')


class DirectedGraph(Generic[T]):
    """
    @brief Реализация направленного графа с использованием представления списками смежности
    
    @details Этот класс реализует направленный граф, где рёбра имеют направление.
             Граф представлен внутренне с использованием списка смежности для
             эффективного поиска рёбер и обходов.
    
    @tparam T Тип данных, хранящихся в вершинах
    """
    
    def __init__(self):
        """
        @brief Конструирует пустой направленный граф
        """
        self._adjacency_list: Dict[T, Set[T]] = defaultdict(set)
        self._vertices: Set[T] = set()
        self._edge_count: int = 0
    
    def add_vertex(self, vertex: T) -> bool:
        """
        @brief Добавляет вершину в граф
        
        @param vertex Значение вершины для добавления
        @return True если вершина была добавлена, False если она уже существовала
        
        @code
        graph = DirectedGraph()
        graph.add_vertex("A")
        graph.add_vertex("B")
        @endcode
        """
        if vertex in self._vertices:
            return False
        self._vertices.add(vertex)
        if vertex not in self._adjacency_list:
            self._adjacency_list[vertex] = set()
        return True
    
    def remove_vertex(self, vertex: T) -> bool:
        """
        @brief Удаляет вершину и все её инцидентные рёбра из графа
        
        @param vertex Вершина для удаления
        @return True если вершина была удалена, False если она не существовала
        
        @note Все рёбра, соединённые с этой вершиной, также удаляются
        """
        if vertex not in self._vertices:
            return False
        
        # Удалить все исходящие рёбра из этой вершины
        self._edge_count -= len(self._adjacency_list[vertex])
        
        # Удалить все входящие рёбра в эту вершину
        for v in self._vertices:
            if vertex in self._adjacency_list[v]:
                self._adjacency_list[v].remove(vertex)
                self._edge_count -= 1
        
        # Удалить вершину
        self._vertices.remove(vertex)
        del self._adjacency_list[vertex]
        
        return True
    
    def add_edge(self, source: T, target: T) -> bool:
        """
        @brief Добавляет направленное ребро от источника к цели
        
        @param source Вершина-источник
        @param target Вершина-цель
        @return True если ребро было добавлено, False если оно уже существовало
        
        @throws ValueError если какая-либо из вершин не существует в графе
        
        @code
        graph.add_edge("A", "B")  # Добавляет ребро A -> B
        @endcode
        """
        if source not in self._vertices or target not in self._vertices:
            raise ValueError("Both vertices must exist in the graph")
        
        if target in self._adjacency_list[source]:
            return False
        
        self._adjacency_list[source].add(target)
        self._edge_count += 1
        return True
    
    def remove_edge(self, source: T, target: T) -> bool:
        """
        @brief Удаляет направленное ребро от источника к цели
        
        @param source Вершина-источник
        @param target Вершина-цель
        @return True если ребро было удалено, False если оно не существовало
        """
        if source not in self._vertices or target not in self._vertices:
            return False
        
        if target not in self._adjacency_list[source]:
            return False
        
        self._adjacency_list[source].remove(target)
        self._edge_count -= 1
        return True
    
    def has_vertex(self, vertex: T) -> bool:
        """
        @brief Проверяет, существует ли вершина в графе
        
        @param vertex Вершина для проверки
        @return True если вершина существует, False в противном случае
        """
        return vertex in self._vertices
    
    def has_edge(self, source: T, target: T) -> bool:
        """
        @brief Проверяет, существует ли направленное ребро от источника к цели
        
        @param source Вершина-источник
        @param target Вершина-цель
        @return True если ребро существует, False в противном случае
        """
        if source not in self._vertices or target not in self._vertices:
            return False
        return target in self._adjacency_list[source]
    
    def vertex_count(self) -> int:
        """
        @brief Возвращает количество вершин в графе
        
        @return Количество вершин
        """
        return len(self._vertices)
    
    def edge_count(self) -> int:
        """
        @brief Возвращает количество рёбер в графе
        
        @return Количество рёбер
        """
        return self._edge_count
    
    def out_degree(self, vertex: T) -> int:
        """
        @brief Вычисляет исходящую степень вершины (количество исходящих рёбер)
        
        @param vertex Вершина для проверки
        @return Количество исходящих рёбер
        
        @throws ValueError если вершина не существует
        """
        if vertex not in self._vertices:
            raise ValueError(f"Vertex {vertex} does not exist in the graph")
        return len(self._adjacency_list[vertex])
    
    def in_degree(self, vertex: T) -> int:
        """
        @brief Вычисляет входящую степень вершины (количество входящих рёбер)
        
        @param vertex Вершина для проверки
        @return Количество входящих рёбер
        
        @throws ValueError если вершина не существует
        """
        if vertex not in self._vertices:
            raise ValueError(f"Vertex {vertex} does not exist in the graph")
        
        count = 0
        for v in self._vertices:
            if vertex in self._adjacency_list[v]:
                count += 1
        return count
    
    def degree(self, vertex: T) -> int:
        """
        @brief Вычисляет общую степень вершины (входящая степень + исходящая степень)
        
        @param vertex Вершина для проверки
        @return Общая степень
        """
        return self.in_degree(vertex) + self.out_degree(vertex)
    
    def get_adjacent_vertices(self, vertex: T) -> Set[T]:
        """
        @brief Получает все вершины, смежные с данной вершиной (исходящие рёбра)
        
        @param vertex Вершина-источник
        @return Множество смежных вершин
        
        @throws ValueError если вершина не существует
        """
        if vertex not in self._vertices:
            raise ValueError(f"Vertex {vertex} does not exist in the graph")
        return self._adjacency_list[vertex].copy()
    
    def vertices(self) -> Iterator[T]:
        """
        @brief Итератор по всем вершинам в графе
        
        @return Итератор вершин
        
        @code
        for vertex in graph.vertices():
            print(vertex)
        @endcode
        """
        return iter(self._vertices)
    
    def edges(self) -> Iterator[Tuple[T, T]]:
        """
        @brief Итератор по всем рёбрам в графе
        
        @return Итератор кортежей (источник, цель)
        
        @code
        for source, target in graph.edges():
            print(f"{source} -> {target}")
        @endcode
        """
        for source in self._vertices:
            for target in self._adjacency_list[source]:
                yield (source, target)
    
    def incident_edges(self, vertex: T) -> Iterator[Tuple[T, T]]:
        """
        @brief Итератор по всем рёбрам, инцидентным вершине (как входящим, так и исходящим)
        
        @param vertex Вершина для получения инцидентных рёбер
        @return Итератор кортежей (источник, цель)
        
        @throws ValueError если вершина не существует
        """
        if vertex not in self._vertices:
            raise ValueError(f"Vertex {vertex} does not exist in the graph")
        
        # Исходящие рёбра
        for target in self._adjacency_list[vertex]:
            yield (vertex, target)
        
        # Входящие рёбра
        for source in self._vertices:
            if source != vertex and vertex in self._adjacency_list[source]:
                yield (source, vertex)
    
    def outgoing_edges(self, vertex: T) -> Iterator[Tuple[T, T]]:
        """
        @brief Итератор по исходящим рёбрам из вершины
        
        @param vertex Вершина-источник
        @return Итератор кортежей (источник, цель)
        
        @throws ValueError если вершина не существует
        """
        if vertex not in self._vertices:
            raise ValueError(f"Vertex {vertex} does not exist in the graph")
        
        for target in self._adjacency_list[vertex]:
            yield (vertex, target)
    
    def incoming_edges(self, vertex: T) -> Iterator[Tuple[T, T]]:
        """
        @brief Итератор по входящим рёбрам в вершину
        
        @param vertex Вершина-цель
        @return Итератор кортежей (источник, цель)
        
        @throws ValueError если вершина не существует
        """
        if vertex not in self._vertices:
            raise ValueError(f"Vertex {vertex} does not exist in the graph")
        
        for source in self._vertices:
            if vertex in self._adjacency_list[source]:
                yield (source, vertex)
    
    def adjacent_vertices(self, vertex: T) -> Iterator[T]:
        """
        @brief Итератор по вершинам, смежным с данной вершиной (через исходящие рёбра)
        
        @param vertex Вершина-источник
        @return Итератор смежных вершин
        
        @throws ValueError если вершина не существует
        """
        if vertex not in self._vertices:
            raise ValueError(f"Vertex {vertex} does not exist in the graph")
        
        return iter(self._adjacency_list[vertex])
    
    def clear(self):
        """
        @brief Удаляет все вершины и рёбра из графа
        """
        self._adjacency_list.clear()
        self._vertices.clear()
        self._edge_count = 0
    
    def is_empty(self) -> bool:
        """
        @brief Проверяет, пуст ли граф (нет вершин)
        
        @return True если граф пуст, False в противном случае
        """
        return len(self._vertices) == 0
    
    def __str__(self) -> str:
        """
        @brief Строковое представление графа
        
        @return Строка, описывающая структуру графа
        """
        result = f"DirectedGraph(vertices={self.vertex_count()}, edges={self.edge_count()})\n"
        result += "Adjacency List:\n"
        for vertex in sorted(self._vertices, key=str):
            neighbors = sorted(self._adjacency_list[vertex], key=str)
            result += f"  {vertex} -> {neighbors}\n"
        return result
    
    def __repr__(self) -> str:
        """
        @brief Детальное представление графа
        
        @return Строковое представление
        """
        return self.__str__()
    
    def __eq__(self, other) -> bool:
        """
        @brief Сравнение графов на равенство
        
        @param other Другой DirectedGraph
        @return True если графы имеют одинаковые вершины и рёбра
        """
        if not isinstance(other, DirectedGraph):
            return False
        
        if self._vertices != other._vertices:
            return False
        
        if self._edge_count != other._edge_count:
            return False
        
        for vertex in self._vertices:
            if self._adjacency_list[vertex] != other._adjacency_list[vertex]:
                return False
        
        return True
    
    def __ne__(self, other) -> bool:
        """
        @brief Сравнение на неравенство
        
        @param other Другой DirectedGraph
        @return True если графы различны
        """
        return not self.__eq__(other)


