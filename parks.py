# All 63 officially designated U.S. National Parks, organized by region.
# For any other NPS site (monuments, seashores, recreation areas, etc.)
# use the search_parks tool with a name or keyword.

PARK_CODES: dict[str, str] = {

    # --- Northeast ---
    "acad": "Acadia National Park",                         # Maine
    "neri": "New River Gorge National Park & Preserve",     # West Virginia
    "shen": "Shenandoah National Park",                     # Virginia
    "viis": "Virgin Islands National Park",                 # U.S. Virgin Islands

    # --- Southeast ---
    "bisc": "Biscayne National Park",                       # Florida
    "cong": "Congaree National Park",                       # South Carolina
    "drto": "Dry Tortugas National Park",                   # Florida
    "ever": "Everglades National Park",                     # Florida
    "grsm": "Great Smoky Mountains National Park",          # NC / Tennessee
    "hosp": "Hot Springs National Park",                    # Arkansas
    "maca": "Mammoth Cave National Park",                   # Kentucky

    # --- Midwest ---
    "cuva": "Cuyahoga Valley National Park",                # Ohio
    "indu": "Indiana Dunes National Park",                  # Indiana
    "isro": "Isle Royale National Park",                    # Michigan
    "jeff": "Gateway Arch National Park",                   # Missouri
    "voya": "Voyageurs National Park",                      # Minnesota

    # --- Great Plains ---
    "badl": "Badlands National Park",                       # South Dakota
    "thro": "Theodore Roosevelt National Park",             # North Dakota
    "wica": "Wind Cave National Park",                      # South Dakota

    # --- Rocky Mountain ---
    "blca": "Black Canyon Of The Gunnison National Park",   # Colorado
    "brca": "Bryce Canyon National Park",                   # Utah
    "cany": "Canyonlands National Park",                    # Utah
    "care": "Capitol Reef National Park",                   # Utah
    "grte": "Grand Teton National Park",                    # Wyoming
    "grsa": "Great Sand Dunes National Park & Preserve",    # Colorado
    "meve": "Mesa Verde National Park",                     # Colorado
    "romo": "Rocky Mountain National Park",                 # Colorado
    "yell": "Yellowstone National Park",                    # WY / MT / ID
    "zion": "Zion National Park",                           # Utah

    # --- Southwest ---
    "arch": "Arches National Park",                         # Utah
    "bibe": "Big Bend National Park",                       # Texas
    "cave": "Carlsbad Caverns National Park",               # New Mexico
    "deva": "Death Valley National Park",                   # CA / Nevada
    "grca": "Grand Canyon National Park",                   # Arizona
    "grba": "Great Basin National Park",                    # Nevada
    "gumo": "Guadalupe Mountains National Park",            # Texas
    "pefo": "Petrified Forest National Park",               # Arizona
    "sagu": "Saguaro National Park",                        # Arizona
    "whsa": "White Sands National Park",                    # New Mexico

    # --- California ---
    "chis": "Channel Islands National Park",
    "jotr": "Joshua Tree National Park",
    "kica": "Kings Canyon National Park",
    "lavo": "Lassen Volcanic National Park",
    "pinn": "Pinnacles National Park",
    "redw": "Redwood National & State Parks",
    "sequ": "Sequoia National Park",
    "yose": "Yosemite National Park",

    # --- Pacific Northwest ---
    "crla": "Crater Lake National Park",                    # Oregon
    "mora": "Mount Rainier National Park",                  # Washington
    "noca": "North Cascades National Park",                 # Washington
    "olym": "Olympic National Park",                        # Washington

    # --- Hawaii ---
    "hale": "Haleakalā National Park",
    "havo": "Hawaiʻi Volcanoes National Park",

    # --- Alaska ---
    "dena": "Denali National Park & Preserve",
    "gaar": "Gates of the Arctic National Park & Preserve",
    "glac": "Glacier National Park",                        # Montana (not Alaska — see note)
    "glba": "Glacier Bay National Park & Preserve",         # Alaska
    "katm": "Katmai National Park & Preserve",
    "kefj": "Kenai Fjords National Park",
    "kova": "Kobuk Valley National Park",
    "lacl": "Lake Clark National Park & Preserve",
    "wrst": "Wrangell-St. Elias National Park & Preserve",

    # --- Pacific Territories ---
    "npsa": "National Park of American Samoa",
}

# Reverse lookup: full name (case-insensitive) → park code
_NAME_TO_CODE: dict[str, str] = {name.lower(): code for code, name in PARK_CODES.items()}


def get_park_code(name: str) -> str | None:
    """Return the park code for a given park name, or None if not found."""
    return _NAME_TO_CODE.get(name.lower())
