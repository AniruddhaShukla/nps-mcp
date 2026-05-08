# NPS MCP Server

A [Model Context Protocol (MCP)](https://modelcontextprotocol.io) server that gives Claude (or any MCP-compatible AI client) access to the [National Park Service API](https://www.nps.gov/subjects/developer/api-documentation.htm). Ask questions about parks, alerts, campgrounds, events, parking, and more — all in natural language.

---

## Prerequisites

- **Python 3.11+**
- **An NPS API key** — free, get one at [https://www.nps.gov/subjects/developer/get-started.htm](https://www.nps.gov/subjects/developer/get-started.htm)

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/AniruddhaShukla/nps-mcp.git
cd nps-mcp

# 2. Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Configuration

```bash
# Copy the example env file
cp .env.example .env

# Open .env and replace the placeholder with your real API key
# NPS_API_KEY=your_api_key_here
```

Your `.env` file is listed in `.gitignore` and will never be committed.

---

## Running the Server

```bash
python server.py
```

The server communicates over **stdio** (standard MCP transport) and stays running until you stop it. You don't interact with it directly — your MCP client does.

---

## Connecting to Claude Desktop

1. Open your Claude Desktop config file:
   - **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

2. Add this block inside the `"mcpServers"` object (create the object if it doesn't exist):

```json
{
  "mcpServers": {
    "national-parks": {
      "command": "/absolute/path/to/.venv/bin/python",
      "args": ["/absolute/path/to/nps-mcp/server.py"],
      "env": {
        "NPS_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

Replace the paths with the actual absolute paths on your machine. Using the env block here means you don't even need the `.env` file — the key is passed directly.

3. Restart Claude Desktop. To verify it's working, click the **paperclip / attachment icon** in the chat input bar, then select **Connectors** — you should see `national-parks` listed with a blue toggle indicating it's running. You can enable or disable it per conversation from there.

---

## Connecting to Claude Code

```bash
claude mcp add national-parks -- /absolute/path/to/.venv/bin/python /absolute/path/to/nps-mcp/server.py
```

Then set the environment variable in your shell before running Claude Code:

```bash
export NPS_API_KEY=your_api_key_here
claude
```

---

## Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector python server.py
```

This opens a browser UI where you can call each tool manually and inspect responses.

---

## Available Tools

### 🗺️ Trip Planning
| Tool | Description |
|------|-------------|
| `plan_visit` | **One-stop trip planner** — fetches alerts, fees, visitor centers, things to do, campgrounds, and events for a park in a single call |
| `list_known_parks` | List all 63 park codes and full names |
| `search_parks` | Search parks by name or keyword, optionally filtered by state |
| `get_park` | Full details for a specific park (description, hours, directions, weather) |

### 🚨 Alerts & News
| Tool | Description |
|------|-------------|
| `get_park_alerts` | Current closures, dangers, cautions, and notices |
| `get_news_releases` | Recent press releases from a park |
| `get_road_events` | Road closures and construction zones |

### 🏛️ Facilities
| Tool | Description |
|------|-------------|
| `get_visitor_centers` | Visitor center hours and contact info |
| `get_parking_lots` | Parking lot capacity, accessibility, and live occupancy |
| `get_campgrounds` | Campground details, fees, and reservations |
| `get_webcams` | Live webcam feeds |

### 🥾 Activities & Experiences
| Tool | Description |
|------|-------------|
| `get_things_to_do` | Recommended activities at a park |
| `get_tours` | Guided tours available at a park |
| `get_events` | Upcoming ranger programs and park events |
| `get_activities` | Browse all activity categories (hiking, kayaking, stargazing, etc.) |
| `get_activities_parks` | **Reverse lookup** — find parks that offer a specific activity |
| `get_topics` | Browse all topic categories (Civil War, geology, Indigenous culture, etc.) |
| `get_topics_parks` | **Reverse lookup** — find parks associated with a specific topic |

### ♿ Amenities
| Tool | Description |
|------|-------------|
| `get_amenities` | Browse all amenity types (restrooms, fire pits, picnic tables, etc.) |
| `get_amenities_places` | Find places within a park that have a specific amenity |
| `get_amenities_visitor_centers` | Find visitor centers with a specific amenity |

### 🎟️ Fees & Passes
| Tool | Description |
|------|-------------|
| `get_fees_passes` | Entrance fees and pass information |

### 📸 Multimedia
| Tool | Description |
|------|-------------|
| `get_photo_galleries` | Photo galleries published by parks |
| `get_videos` | Video content from parks |
| `get_audio` | Audio tours and recordings |

### 📚 Educational Content
| Tool | Description |
|------|-------------|
| `get_places` | Notable landmarks and places within a park |
| `get_people` | Historical figures and conservationists associated with a park |
| `get_articles` | Educational articles published by the park |
| `get_lesson_plans` | Teacher lesson plans related to a park |
| `get_passport_stamp_locations` | Where to collect National Park Passport stamps |

---

## Known Park Codes

All 63 officially designated U.S. National Parks are pre-mapped. For any other NPS site (monuments, seashores, recreation areas, etc.) use `search_parks` to find its code.

**Northeast**
| Code | Park |
|------|------|
| `acad` | Acadia National Park |
| `neri` | New River Gorge National Park & Preserve |
| `shen` | Shenandoah National Park |
| `viis` | Virgin Islands National Park |

**Southeast**
| Code | Park |
|------|------|
| `bisc` | Biscayne National Park |
| `cong` | Congaree National Park |
| `drto` | Dry Tortugas National Park |
| `ever` | Everglades National Park |
| `grsm` | Great Smoky Mountains National Park |
| `hosp` | Hot Springs National Park |
| `maca` | Mammoth Cave National Park |

**Midwest**
| Code | Park |
|------|------|
| `cuva` | Cuyahoga Valley National Park |
| `indu` | Indiana Dunes National Park |
| `isro` | Isle Royale National Park |
| `jeff` | Gateway Arch National Park |
| `voya` | Voyageurs National Park |

**Great Plains**
| Code | Park |
|------|------|
| `badl` | Badlands National Park |
| `thro` | Theodore Roosevelt National Park |
| `wica` | Wind Cave National Park |

**Rocky Mountain**
| Code | Park |
|------|------|
| `blca` | Black Canyon Of The Gunnison National Park |
| `brca` | Bryce Canyon National Park |
| `cany` | Canyonlands National Park |
| `care` | Capitol Reef National Park |
| `grsa` | Great Sand Dunes National Park & Preserve |
| `grte` | Grand Teton National Park |
| `meve` | Mesa Verde National Park |
| `romo` | Rocky Mountain National Park |
| `yell` | Yellowstone National Park |
| `zion` | Zion National Park |

**Southwest**
| Code | Park |
|------|------|
| `arch` | Arches National Park |
| `bibe` | Big Bend National Park |
| `cave` | Carlsbad Caverns National Park |
| `deva` | Death Valley National Park |
| `grca` | Grand Canyon National Park |
| `grba` | Great Basin National Park |
| `gumo` | Guadalupe Mountains National Park |
| `pefo` | Petrified Forest National Park |
| `sagu` | Saguaro National Park |
| `whsa` | White Sands National Park |

**California**
| Code | Park |
|------|------|
| `chis` | Channel Islands National Park |
| `jotr` | Joshua Tree National Park |
| `kica` | Kings Canyon National Park |
| `lavo` | Lassen Volcanic National Park |
| `pinn` | Pinnacles National Park |
| `redw` | Redwood National & State Parks |
| `sequ` | Sequoia National Park |
| `yose` | Yosemite National Park |

**Pacific Northwest**
| Code | Park |
|------|------|
| `crla` | Crater Lake National Park |
| `mora` | Mount Rainier National Park |
| `noca` | North Cascades National Park |
| `olym` | Olympic National Park |

**Hawaii**
| Code | Park |
|------|------|
| `hale` | Haleakalā National Park |
| `havo` | Hawaiʻi Volcanoes National Park |

**Alaska**
| Code | Park |
|------|------|
| `dena` | Denali National Park & Preserve |
| `gaar` | Gates of the Arctic National Park & Preserve |
| `glba` | Glacier Bay National Park & Preserve |
| `katm` | Katmai National Park & Preserve |
| `kefj` | Kenai Fjords National Park |
| `kova` | Kobuk Valley National Park |
| `lacl` | Lake Clark National Park & Preserve |
| `wrst` | Wrangell-St. Elias National Park & Preserve |

**Other**
| Code | Park |
|------|------|
| `glac` | Glacier National Park (Montana) |
| `npsa` | National Park of American Samoa |

---

## Example Queries

Once connected to Claude, try asking:

**Trip Planning**
- *"Help me plan a visit to Yellowstone National Park."*
- *"I'm visiting the Grand Canyon next week — what should I know?"*

**Alerts & Conditions**
- *"Are there any closures or alerts at Yellowstone right now?"*
- *"Are there road closures at Glacier National Park?"*

**Activities**
- *"Which national parks offer stargazing?"*
- *"Where can I go kayaking in a national park?"*
- *"What are the best things to do at Zion?"*

**History & Topics**
- *"Which parks relate to Civil War history?"*
- *"Find parks connected to Indigenous culture."*

**Facilities & Accessibility**
- *"Find accessible restroom locations at Yellowstone."*
- *"What visitor centers are in Grand Canyon and when are they open?"*
- *"Show me parking lots at Yellowstone and their occupancy."*

**General Discovery**
- *"What national parks are in Utah?"*
- *"Find campgrounds in Yosemite."*
- *"What are the entrance fees for the Grand Canyon?"*
- *"Does Yellowstone have any live webcams?"*

---

## License

This project is released under the [MIT License](LICENSE) — free to use, modify, and distribute for any purpose.

The NPS API is a free public service provided by the U.S. National Park Service.
