import asyncio

from sqlalchemy.orm import Session


async def get_outdated_tiles(db: Session):
    pass


async def render_outdated():
    pass


async def mainloop(db: Session):
    """Main loop to render outdated tiles."""
    while True:
        # Get the list of outdated tiles
        # outdated_tiles = get_outdated_tiles()
        # Get the list of tiles to render
        # tiles_to_render = get_tiles_to_render(outdated_tiles)
        # Render the tiles
        # render_tiles(tiles_to_render)
        # Update the database
        # update_database(tiles_to_render)

        # Nothing to do, sleep for a while
        await asyncio.sleep(60)
