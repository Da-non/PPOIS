"""
@file test_graph.py
@brief Модульные тесты для класса DirectedGraph
@details Комплексный набор тестов для реализации DirectedGraph
"""

import unittest
from graph import DirectedGraph


class TestDirectedGraphBasics(unittest.TestCase):
    """Тест базовых операций с графом"""
    
    def test_empty_graph_creation(self):
        """Тест создания пустого графа"""
        graph = DirectedGraph[int]()
        self.assertTrue(graph.is_empty())
        self.assertEqual(graph.vertex_count(), 0)
        self.assertEqual(graph.edge_count(), 0)
    
    def test_add_single_vertex(self):
        """Тест добавления одной вершины"""
        graph = DirectedGraph[str]()
        self.assertTrue(graph.add_vertex("A"))
        self.assertEqual(graph.vertex_count(), 1)
        self.assertFalse(graph.is_empty())
    
    def test_add_duplicate_vertex(self):
        """Тест что добавление дублирующей вершины возвращает False"""
        graph = DirectedGraph[str]()
        self.assertTrue(graph.add_vertex("A"))
        self.assertFalse(graph.add_vertex("A"))
        self.assertEqual(graph.vertex_count(), 1)
    
    def test_add_multiple_vertices(self):
        """Тест добавления множественных вершин"""
        graph = DirectedGraph[str]()
        vertices = ["A", "B", "C", "D"]
        for v in vertices:
            graph.add_vertex(v)
        self.assertEqual(graph.vertex_count(), 4)
    
    def test_has_vertex(self):
        """Тест проверки существования вершины"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        self.assertTrue(graph.has_vertex("A"))
        self.assertFalse(graph.has_vertex("B"))
    
    def test_remove_vertex(self):
        """Тест удаления вершины"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        self.assertTrue(graph.remove_vertex("A"))
        self.assertEqual(graph.vertex_count(), 0)
        self.assertTrue(graph.is_empty())
    
    def test_remove_nonexistent_vertex(self):
        """Тест удаления несуществующей вершины returns False"""
        graph = DirectedGraph[str]()
        self.assertFalse(graph.remove_vertex("A"))


class TestDirectedGraphEdges(unittest.TestCase):
    """Тест операций с рёбрами"""
    
    def test_add_edge(self):
        """Тест добавления ребра"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        self.assertTrue(graph.add_edge("A", "B"))
        self.assertEqual(graph.edge_count(), 1)
    
    def test_add_edge_nonexistent_vertex_raises(self):
        """При тестировании добавления ребра с несуществующей вершиной возникает ошибка ValueError"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        with self.assertRaises(ValueError):
            graph.add_edge("A", "B")
    
    def test_add_duplicate_edge(self):
        """Тест что добавление дублирующего ребра возвращает False"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        self.assertTrue(graph.add_edge("A", "B"))
        self.assertFalse(graph.add_edge("A", "B"))
        self.assertEqual(graph.edge_count(), 1)
    
    def test_has_edge(self):
        """Тест проверки существования ребра"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_edge("A", "B")
        self.assertTrue(graph.has_edge("A", "B"))
        self.assertFalse(graph.has_edge("B", "A"))  # Directed graph
    
    def test_remove_edge(self):
        """Протестируйте удаление ребра"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_edge("A", "B")
        self.assertTrue(graph.remove_edge("A", "B"))
        self.assertEqual(graph.edge_count(), 0)
        self.assertFalse(graph.has_edge("A", "B"))
    
    def test_remove_nonexistent_edge(self):
        """Тест удаления несуществующего ребра returns False"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        self.assertFalse(graph.remove_edge("A", "B"))
    
    def test_self_loop(self):
        """Test adding self-loop edge"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        self.assertTrue(graph.add_edge("A", "A"))
        self.assertTrue(graph.has_edge("A", "A"))
        self.assertEqual(graph.edge_count(), 1)


class TestDirectedGraphDegrees(unittest.TestCase):
    """Тест вычисления степеней"""
    
    def test_out_degree_zero(self):
        """Test степени изолированности вершины"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        self.assertEqual(graph.out_degree("A"), 0)
    
    def test_out_degree_nonzero(self):
        """Тест вычисления исходящей степени"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        self.assertEqual(graph.out_degree("A"), 2)
    
    def test_in_degree_zero(self):
        """Проверка степени изолированности вершины"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        self.assertEqual(graph.in_degree("A"), 0)
    
    def test_in_degree_nonzero(self):
        """Тест вычисления входящей степени"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("B", "A")
        graph.add_edge("C", "A")
        self.assertEqual(graph.in_degree("A"), 2)
    
    def test_total_degree(self):
        """Тест вычисления общей степени"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("A", "B")  # A out
        graph.add_edge("C", "A")  # A in
        self.assertEqual(graph.degree("A"), 2)
    
    def test_degree_nonexistent_vertex_raises(self):
        """Проверка степени несуществующей вершины приводит к возникновению ValueError"""
        graph = DirectedGraph[str]()
        with self.assertRaises(ValueError):
            graph.out_degree("A")
        with self.assertRaises(ValueError):
            graph.in_degree("A")


class TestDirectedGraphIterators(unittest.TestCase):
    """Тестовые итераторы"""
    
    def test_vertices_iterator(self):
        """Тестовое повторение по вершинам"""
        graph = DirectedGraph[str]()
        vertices = ["A", "B", "C"]
        for v in vertices:
            graph.add_vertex(v)
        
        result = list(graph.vertices())
        self.assertEqual(set(result), set(vertices))
    
    def test_edges_iterator(self):
        """Тестовое повторение по ребрам"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        
        edges = list(graph.edges())
        self.assertEqual(len(edges), 2)
        self.assertIn(("A", "B"), edges)
        self.assertIn(("B", "C"), edges)
    
    def test_adjacent_vertices_iterator(self):
        """Тестовое повторение по соседним вершинам"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        
        adjacent = set(graph.adjacent_vertices("A"))
        self.assertEqual(adjacent, {"B", "C"})
    
    def test_incident_edges_iterator(self):
        """Test iterating over incident edges"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("A", "B")
        graph.add_edge("C", "A")
        
        incident = list(graph.incident_edges("A"))
        self.assertEqual(len(incident), 2)
        self.assertIn(("A", "B"), incident)
        self.assertIn(("C", "A"), incident)
    
    def test_outgoing_edges_iterator(self):
        """Test iterating over outgoing edges"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        graph.add_edge("B", "A")
        
        outgoing = list(graph.outgoing_edges("A"))
        self.assertEqual(len(outgoing), 2)
        self.assertIn(("A", "B"), outgoing)
        self.assertIn(("A", "C"), outgoing)
    
    def test_incoming_edges_iterator(self):
        """Test iterating over incoming edges"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("B", "A")
        graph.add_edge("C", "A")
        graph.add_edge("A", "B")
        
        incoming = list(graph.incoming_edges("A"))
        self.assertEqual(len(incoming), 2)
        self.assertIn(("B", "A"), incoming)
        self.assertIn(("C", "A"), incoming)
    
    def test_empty_iterators(self):
        """Тест итераторов на пустом графе"""
        graph = DirectedGraph[str]()
        self.assertEqual(list(graph.vertices()), [])
        self.assertEqual(list(graph.edges()), [])


class TestDirectedGraphRemoval(unittest.TestCase):
    """Тест операций удаления"""
    
    def test_remove_vertex_removes_edges(self):
        """Проверьте, что удаление вершины также приводит к удалению ее ребер"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A")
        
        initial_edges = graph.edge_count()
        graph.remove_vertex("B")
        
        self.assertLess(graph.edge_count(), initial_edges)
        self.assertFalse(graph.has_vertex("B"))
        self.assertFalse(graph.has_edge("A", "B"))
        self.assertFalse(graph.has_edge("B", "C"))
    
    def test_clear(self):
        """Протестируйте очистку графа"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_edge("A", "B")
        
        graph.clear()
        
        self.assertTrue(graph.is_empty())
        self.assertEqual(graph.vertex_count(), 0)
        self.assertEqual(graph.edge_count(), 0)


class TestDirectedGraphComparison(unittest.TestCase):
    """Тест операций сравнения графов"""
    
    def test_equality_empty_graphs(self):
        """Тест равенства пустых графов"""
        g1 = DirectedGraph[str]()
        g2 = DirectedGraph[str]()
        self.assertEqual(g1, g2)
    
    def test_equality_same_graphs(self):
        """Проверьте равенство идентичных графов"""
        g1 = DirectedGraph[str]()
        g2 = DirectedGraph[str]()
        
        for g in [g1, g2]:
            g.add_vertex("A")
            g.add_vertex("B")
            g.add_edge("A", "B")
        
        self.assertEqual(g1, g2)
    
    def test_inequality_different_vertices(self):
        """Тест неравенства с разными вершинами"""
        g1 = DirectedGraph[str]()
        g2 = DirectedGraph[str]()
        
        g1.add_vertex("A")
        g2.add_vertex("B")
        
        self.assertNotEqual(g1, g2)
    
    def test_inequality_different_edges(self):
        """Тест неравенства с разными рёбрами"""
        g1 = DirectedGraph[str]()
        g2 = DirectedGraph[str]()
        
        for g in [g1, g2]:
            g.add_vertex("A")
            g.add_vertex("B")
        
        g1.add_edge("A", "B")
        g2.add_edge("B", "A")
        
        self.assertNotEqual(g1, g2)
    
    def test_inequality_with_non_graph(self):
        """Тест неравенства с не-графовым объектом"""
        g = DirectedGraph[str]()
        self.assertNotEqual(g, "not a graph")
        self.assertNotEqual(g, 42)
        self.assertNotEqual(g, [])


class TestDirectedGraphHelperMethods(unittest.TestCase):
    """Тест вспомогательных методов"""
    
    def test_get_adjacent_vertices(self):
        """Проверьте получение смежных вершин"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("A", "B")
        graph.add_edge("A", "C")
        
        adjacent = graph.get_adjacent_vertices("A")
        self.assertEqual(adjacent, {"B", "C"})
    
    def test_get_adjacent_vertices_nonexistent_raises(self):
        """Тест на получение смежных вершин несуществующей вершины вызывает ошибку ValueError"""
        graph = DirectedGraph[str]()
        with self.assertRaises(ValueError):
            graph.get_adjacent_vertices("A")
    
    def test_str_representation(self):
        """Тест строкового представления"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_edge("A", "B")
        
        string = str(graph)
        self.assertIn("DirectedGraph", string)
        self.assertIn("vertices=2", string)
        self.assertIn("edges=1", string)


class TestDirectedGraphCustomTypes(unittest.TestCase):
    """Тест графа с пользовательскими типами"""
    
    def test_integer_graph(self):
        """Тест графа с целыми числами"""
        graph = DirectedGraph[int]()
        graph.add_vertex(1)
        graph.add_vertex(2)
        graph.add_edge(1, 2)
        
        self.assertTrue(graph.has_vertex(1))
        self.assertTrue(graph.has_edge(1, 2))
    
    def test_tuple_graph(self):
        """Тест графа с кортежами"""
        graph = DirectedGraph[tuple]()
        v1 = (1, 2)
        v2 = (3, 4)
        
        graph.add_vertex(v1)
        graph.add_vertex(v2)
        graph.add_edge(v1, v2)
        
        self.assertTrue(graph.has_vertex(v1))
        self.assertTrue(graph.has_edge(v1, v2))


class TestDirectedGraphEdgeCases(unittest.TestCase):
    """Тестируйте пограничные случаи и условия возникновения ошибок"""
    
    def test_large_graph(self):
        """Тест с длинным графом"""
        graph = DirectedGraph[int]()
        n = 100
        
        # Add vertices
        for i in range(n):
            graph.add_vertex(i)
        
        # Add edges in a chain
        for i in range(n - 1):
            graph.add_edge(i, i + 1)
        
        self.assertEqual(graph.vertex_count(), n)
        self.assertEqual(graph.edge_count(), n - 1)
    
    def test_fully_connected_small_graph(self):
        """Test fully connected graph"""
        graph = DirectedGraph[int]()
        vertices = [1, 2, 3]
        
        for v in vertices:
            graph.add_vertex(v)
        
        # Add all possible edges
        for v1 in vertices:
            for v2 in vertices:
                if v1 != v2:
                    graph.add_edge(v1, v2)
        
        # n * (n - 1) edges in fully connected directed graph
        self.assertEqual(graph.edge_count(), len(vertices) * (len(vertices) - 1))
    
    def test_isolated_vertices(self):
        """Тестовый граф с изолированными вершинами"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        
        # No edges
        self.assertEqual(graph.edge_count(), 0)
        self.assertEqual(graph.out_degree("A"), 0)
        self.assertEqual(graph.in_degree("A"), 0)
    
    def test_multiple_self_loops_same_vertex(self):
        """Проверьте, не добавляются ли повторяющиеся циклы self-loops"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        
        self.assertTrue(graph.add_edge("A", "A"))
        self.assertFalse(graph.add_edge("A", "A"))
        self.assertEqual(graph.edge_count(), 1)


class TestDirectedGraphComplexScenarios(unittest.TestCase):
    """Тестируйте сложные сценарии"""
    
    def test_cycle_detection_simple(self):
        """Протестируйте простой цикл на графе"""
        graph = DirectedGraph[str]()
        graph.add_vertex("A")
        graph.add_vertex("B")
        graph.add_vertex("C")
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "A")
        
        self.assertTrue(graph.has_edge("A", "B"))
        self.assertTrue(graph.has_edge("B", "C"))
        self.assertTrue(graph.has_edge("C", "A"))
    
    def test_path_existence(self):
        """Проверка тестового пути"""
        graph = DirectedGraph[str]()
        vertices = ["A", "B", "C", "D"]
        for v in vertices:
            graph.add_vertex(v)
        
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")
        graph.add_edge("C", "D")
        
        # There's a path A -> B -> C -> D
        self.assertTrue(graph.has_edge("A", "B"))
        self.assertTrue(graph.has_edge("B", "C"))
        self.assertTrue(graph.has_edge("C", "D"))
        # But no direct edge from A to D
        self.assertFalse(graph.has_edge("A", "D"))


if __name__ == "__main__":
    unittest.main()
