import overpy

api = overpy.Overpass()

# Bounding box for Copenhagen
bbox = (55.59, 12.53, 55.72, 12.63)  # min_lat, min_lon, max_lat, max_lon

query = f"""
node["shop"="bakery"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
out center;
"""

result = api.query(query)
print(f"Found {len(result.nodes)} bakeries.")
for node in result.nodes[:5]:  # show first 5
    print(node.tags.get("name"), node.lat, node.lon)

