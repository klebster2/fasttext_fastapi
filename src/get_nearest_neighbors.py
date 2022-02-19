from .word_neighbors import (
        Word_Neighbors_Request,
        Word_Neighbors_Response,
)

async def get_word_neighbors(
        word_neighbors_request: Word_Neighbors_Request,
        model=None,
    ) -> Word_Neighbors_Response:
    """
    Parameters
    ----------
    word_neighbors_request: Word_Neighbors_Request

    Returns
    -------
    Word_Neighbors_Response

    See Also
    --------
    ...

    Examples
    --------
    ...
    """
    neighbors = model.get_nearest_neighbors(
            word_neighbors_request.word,
            k=word_neighbors_request.neighbors,
    )
    neighbors_output = []
    for i, neighbor in enumerate(neighbors, 1):
        neighbors_output.append(
            {
                "id": i,
                "neighbor": neighbor[1],
                "score": f"{neighbor[0]:.5f}",
            }
        )
    return Word_Neighbors_Response(
            neighbors_output=neighbors_output,
    )
