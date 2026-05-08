import os
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from parks import PARK_CODES, get_park_code

load_dotenv()

NPS_API_KEY = os.environ.get("NPS_API_KEY")
if not NPS_API_KEY:
    raise ValueError(
        "NPS_API_KEY environment variable is required. "
        "Copy .env.example to .env and add your API key."
    )

BASE_URL = "https://developer.nps.gov/api/v1"

mcp = FastMCP("National Parks Service")


async def nps_get(endpoint: str, params: dict) -> dict:
    params = {k: v for k, v in params.items() if v is not None}
    params["api_key"] = NPS_API_KEY
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()


# ---------------------------------------------------------------------------
# Park discovery tools
# ---------------------------------------------------------------------------

@mcp.tool()
def list_known_parks() -> str:
    """
    List all park codes and their full names that are known to this server.
    Use the park code returned here as the `park_code` argument for other tools.
    """
    lines = [f"{code}: {name}" for code, name in sorted(PARK_CODES.items(), key=lambda x: x[1])]
    return "\n".join(lines)


@mcp.tool()
async def search_parks(query: str, state_code: str = None, limit: int = 10) -> dict:
    """
    Search national parks by name or keyword.

    Args:
        query: Search term, e.g. "yellowstone", "canyon", "redwood".
        state_code: Optional 2-letter US state code to narrow results, e.g. "CA", "WY".
        limit: Maximum number of results to return (default 10, max 50).
    """
    return await nps_get("parks", {"q": query, "stateCode": state_code, "limit": limit, "fields": "images,addresses,contacts,operatingHours,entranceFees"})


@mcp.tool()
async def get_park(park_code: str) -> dict:
    """
    Get detailed information about a specific national park by its park code.

    Args:
        park_code: 4-letter park code, e.g. "yell" for Yellowstone, "grca" for Grand Canyon.
                   Use list_known_parks() to see available codes.
    """
    return await nps_get("parks", {"parkCode": park_code, "fields": "images,addresses,contacts,operatingHours,entranceFees,description,weatherInfo,directionsInfo"})


# ---------------------------------------------------------------------------
# Alerts & news
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_park_alerts(park_code: str) -> dict:
    """
    Get current alerts for a national park (closures, dangers, cautions, informational notices).

    Args:
        park_code: 4-letter park code, e.g. "yell", "acad", "grca".
    """
    return await nps_get("alerts", {"parkCode": park_code})


@mcp.tool()
async def get_news_releases(park_code: str, limit: int = 10) -> dict:
    """
    Get recent news releases and press releases for a national park.

    Args:
        park_code: 4-letter park code, e.g. "yell", "yose".
        limit: Maximum number of results (default 10).
    """
    return await nps_get("newsreleases", {"parkCode": park_code, "limit": limit})


# ---------------------------------------------------------------------------
# Facilities
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_visitor_centers(park_code: str) -> dict:
    """
    Get visitor center information for a national park, including hours and contacts.

    Args:
        park_code: 4-letter park code, e.g. "yell", "zion".
    """
    return await nps_get("visitorcenters", {"parkCode": park_code})


@mcp.tool()
async def get_parking_lots(park_code: str) -> dict:
    """
    Get parking lot information for a national park, including capacity, accessibility,
    operating hours, and live occupancy status where available.

    Args:
        park_code: 4-letter park code, e.g. "yell", "grca".
    """
    return await nps_get("parkinglots", {"parkCode": park_code})


@mcp.tool()
async def get_campgrounds(park_code: str = None, state_code: str = None, query: str = None, limit: int = 10) -> dict:
    """
    Get campground information for a national park or state, including reservation details,
    amenities, fees, and accessibility.

    Args:
        park_code: Optional 4-letter park code, e.g. "yell", "yose".
        state_code: Optional 2-letter state code, e.g. "WY", "CA".
        query: Optional search term.
        limit: Maximum number of results (default 10).
    """
    return await nps_get("campgrounds", {"parkCode": park_code, "stateCode": state_code, "q": query, "limit": limit})


@mcp.tool()
async def get_webcams(park_code: str = None, query: str = None) -> dict:
    """
    Get live and recorded webcams for a national park.

    Args:
        park_code: Optional 4-letter park code, e.g. "yell", "olym".
        query: Optional search term.
    """
    return await nps_get("webcams", {"parkCode": park_code, "q": query})


# ---------------------------------------------------------------------------
# Activities & experiences
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_events(park_code: str = None, date_start: str = None, date_end: str = None, limit: int = 10) -> dict:
    """
    Get upcoming events at a national park.

    Args:
        park_code: Optional 4-letter park code, e.g. "yose", "shen".
        date_start: Optional start date filter in MM/DD/YYYY format.
        date_end: Optional end date filter in MM/DD/YYYY format.
        limit: Maximum number of results (default 10).
    """
    return await nps_get("events", {"parkCode": park_code, "dateStart": date_start, "dateEnd": date_end, "pageSize": limit})


@mcp.tool()
async def get_things_to_do(park_code: str = None, query: str = None, limit: int = 10) -> dict:
    """
    Get recommended activities and things to do at a national park.

    Args:
        park_code: Optional 4-letter park code, e.g. "grca", "glac".
        query: Optional keyword search, e.g. "hiking", "fishing", "wildlife".
        limit: Maximum number of results (default 10).
    """
    return await nps_get("thingstodo", {"parkCode": park_code, "q": query, "limit": limit})


@mcp.tool()
async def get_tours(park_code: str = None, query: str = None, limit: int = 10) -> dict:
    """
    Get guided tours available at a national park.

    Args:
        park_code: Optional 4-letter park code, e.g. "yose", "grca".
        query: Optional search term.
        limit: Maximum number of results (default 10).
    """
    return await nps_get("tours", {"parkCode": park_code, "q": query, "limit": limit})


@mcp.tool()
async def get_activities(query: str = None) -> dict:
    """
    Get a list of all activity categories available in national parks
    (e.g. hiking, fishing, stargazing, snowshoeing).

    Args:
        query: Optional search term to filter activities.
    """
    return await nps_get("activities", {"q": query})


@mcp.tool()
async def get_topics(query: str = None) -> dict:
    """
    Get a list of all topic categories used to describe national parks
    (e.g. Civil War, geology, women's history).

    Args:
        query: Optional search term to filter topics.
    """
    return await nps_get("topics", {"q": query})


# ---------------------------------------------------------------------------
# Fees & passes
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_fees_passes(park_code: str = None, query: str = None, limit: int = 10) -> dict:
    """
    Get entrance fees and passes information for a national park.

    Args:
        park_code: Optional 4-letter park code, e.g. "yell", "grca".
        query: Optional search term.
        limit: Maximum number of results (default 10).
    """
    return await nps_get("feespasses", {"parkCode": park_code, "q": query, "limit": limit})


# ---------------------------------------------------------------------------
# Road conditions
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_road_events(park_code: str = None, query: str = None) -> dict:
    """
    Get road incidents, construction zones, and closures for a national park.

    Args:
        park_code: Optional 4-letter park code, e.g. "yell", "glac".
        query: Optional search term.
    """
    return await nps_get("roadevents", {"parkCode": park_code, "q": query})


# ---------------------------------------------------------------------------
# Educational & editorial content
# ---------------------------------------------------------------------------

@mcp.tool()
async def get_places(park_code: str = None, query: str = None, limit: int = 10) -> dict:
    """
    Get articles about notable places within a national park (landmarks, viewpoints, etc.).

    Args:
        park_code: Optional 4-letter park code, e.g. "yose", "care".
        query: Optional search term.
        limit: Maximum number of results (default 10).
    """
    return await nps_get("places", {"parkCode": park_code, "q": query, "limit": limit})


@mcp.tool()
async def get_people(park_code: str = None, query: str = None, limit: int = 10) -> dict:
    """
    Get articles about notable people associated with a national park
    (explorers, conservationists, historical figures, etc.).

    Args:
        park_code: Optional 4-letter park code.
        query: Optional search term, e.g. "John Muir".
        limit: Maximum number of results (default 10).
    """
    return await nps_get("people", {"parkCode": park_code, "q": query, "limit": limit})


@mcp.tool()
async def get_articles(park_code: str = None, query: str = None, limit: int = 10) -> dict:
    """
    Get informational articles published by a national park or NPS entity.

    Args:
        park_code: Optional 4-letter park code, e.g. "romo", "dena".
        query: Optional search term.
        limit: Maximum number of results (default 10).
    """
    return await nps_get("articles", {"parkCode": park_code, "q": query, "limit": limit})


@mcp.tool()
async def get_lesson_plans(park_code: str = None, query: str = None, limit: int = 10) -> dict:
    """
    Get educational lesson plans related to a national park (for teachers and students).

    Args:
        park_code: Optional 4-letter park code.
        query: Optional search term, e.g. "geology", "wildlife".
        limit: Maximum number of results (default 10).
    """
    return await nps_get("lessonplans", {"parkCode": park_code, "q": query, "limit": limit})


@mcp.tool()
async def get_passport_stamp_locations(park_code: str = None, query: str = None) -> dict:
    """
    Get locations where visitors can collect National Park Passport stamps.

    Args:
        park_code: Optional 4-letter park code, e.g. "yell", "brca".
        query: Optional search term.
    """
    return await nps_get("passportstamplocations", {"parkCode": park_code, "q": query})


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    mcp.run()
