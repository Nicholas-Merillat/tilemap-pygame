I took inspiration from Terraria when coding the tilemap and rendering it.

Instead of splitting the tilemap into chunks, I just use a big 2D array to store tile locations and ID's, then calculate the visible tiles on screen to render.

This lets you have extremely large worlds with great performance.
