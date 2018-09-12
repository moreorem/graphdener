# -*- coding: utf-8 -*-
# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
"""
Graph utilities
===============

A module containing several graph utility functions.
"""
# TODO: Translate these to Rust methods and call them from the frontend
import numpy as np
import math

try:
    from scipy.sparse import issparse
    from scipy import sparse
except ImportError:
    def issparse(*args, **kwargs):
        return False


def _get_edges(adjacency_mat):
    func = _sparse_get_edges if issparse(adjacency_mat) else _ndarray_get_edges
    return func(adjacency_mat)


def _sparse_get_edges(adjacency_mat):
    return np.concatenate((adjacency_mat.row[:, np.newaxis],
                           adjacency_mat.col[:, np.newaxis]), axis=-1)


def _ndarray_get_edges(adjacency_mat):
    # Get indices of all non zero values
    i, j = np.where(adjacency_mat)

    return np.concatenate((i[:, np.newaxis], j[:, np.newaxis]), axis=-1)


def _get_directed_edges(adjacency_mat):
    func = _sparse_get_edges if issparse(adjacency_mat) else _ndarray_get_edges

    if issparse(adjacency_mat):
        triu = sparse.triu
        tril = sparse.tril
    else:
        triu = np.triu
        tril = np.tril

    upper = triu(adjacency_mat)
    lower = tril(adjacency_mat)

    return np.concatenate((func(upper), func(lower)))


def _straight_line_vertices(adjacency_mat, node_coords, directed=False):
    """
    Generate the vertices for straight lines between nodes.

    If it is a directed graph, it also generates the vertices which can be
    passed to an :class:`ArrowVisual`.

    Parameters
    ----------
    adjacency_mat : array
        The adjacency matrix of the graph
    node_coords : array
        The current coordinates of all nodes in the graph
    directed : bool
        Wether the graph is directed. If this is true it will also generate
        the vertices for arrows which can be passed to :class:`ArrowVisual`.

    Returns
    -------
    vertices : tuple
        Returns a tuple containing containing (`line_vertices`,
        `arrow_vertices`)
    """

    if not issparse(adjacency_mat):
        adjacency_mat = np.asarray(adjacency_mat, float)

    if (adjacency_mat.ndim != 2 or adjacency_mat.shape[0] !=
            adjacency_mat.shape[1]):
        raise ValueError("Adjacency matrix should be square.")

    arrow_vertices = np.array([])

    edges = _get_edges(adjacency_mat)
    line_vertices = node_coords[edges.ravel()]

    if directed:
        arrows = np.array(list(_get_directed_edges(adjacency_mat)))
        arrow_vertices = node_coords[arrows.ravel()]
        arrow_vertices = arrow_vertices.reshape((len(arrow_vertices)/2, 4))

    return line_vertices, arrow_vertices


def _rescale_layout(pos, scale=1):
    """
    Normalize the given coordinate list to the range [0, `scale`].

    Parameters
    ----------
    pos : array
        Coordinate list
    scale : number
        The upperbound value for the coordinates range

    Returns
    -------
    pos : array
        The rescaled (normalized) coordinates in the range [0, `scale`].

    Notes
    -----
    Changes `pos` in place.
    """

    pos -= pos.min(axis=0)
    pos *= scale / pos.max()

    return pos


def create_arrowhead(A, B):
    """
    Use trigonometry to calculate the arrowheads vertex positions according to the edge direction.

    Parameters
    ----------
    A : array
        x,y Starting point of edge
    B : array
        x,y Ending point of edge

    Returns
    -------
    v1, v2 : tuple
        The v1 xy and v2 xy points of the two base vertices of the arrowhead.
    """
    w = 0.005
    h = w * (0.8660254037844386467637)  # sqrt(3)/2
    mag = math.sqrt((B[0] - A[0])**2.0 + (B[1] - A[1])**2.0)

    u0 = (B[0] - A[0]) / (mag)
    u1 = (B[1] - A[1]) / (mag)
    U = [u0, u1]
    V = [-U[1], U[0]]
    v1 = [B[0] - h * U[0] + w * V[0], B[1] - h * U[1] + w * V[1]]
    v2 = [B[0] - h * U[0] - w * V[0], B[1] - h * U[1] - w * V[1]]
    return (v1, v2)


def get_segments_pos(vPos, edgeList):
    return [[vPos[i[0]], vPos[i[1]]] for i in edgeList]
