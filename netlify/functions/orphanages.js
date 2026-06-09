const sampleOrphanages = [
  {
    id: 1,
    name: "Sunshine Orphanage",
    address: "123 Banjara Hills Road",
    city: "Hyderabad",
    state: "Telangana",
    phone: "+91 40 1234 5678",
    email: "info@sunshineorphanage.org",
    needs: "Food, Education, Clothes",
    latitude: 17.4126,
    longitude: 78.4071,
    distance: 2.5
  },
  {
    id: 2,
    name: "Rainbow Children's Home",
    address: "456 Andheri Park Road",
    city: "Mumbai",
    state: "Maharashtra",
    phone: "+91 22 9876 5432",
    email: "contact@rainbowchildrenshome.org",
    needs: "Medicine, Books, Beds",
    latitude: 19.1136,
    longitude: 72.8697,
    distance: 5.1
  },
  {
    id: 3,
    name: "Hope Old Age Home",
    address: "789 Indiranagar Garden Street",
    city: "Bangalore",
    state: "Karnataka",
    phone: "+91 80 5555 7777",
    email: "hope@oldagehome.org",
    needs: "Medicine, Food, Supplies",
    latitude: 12.9784,
    longitude: 77.6408,
    distance: 8.3
  },
  {
    id: 4,
    name: "Grace Orphanage Trust",
    address: "321 T. Nagar Temple Road",
    city: "Chennai",
    state: "Tamil Nadu",
    phone: "+91 44 3333 4444",
    email: "grace@orphanagetrust.org",
    needs: "Education, Clothes, Supplies",
    latitude: 13.0418,
    longitude: 80.2341,
    distance: 12.0
  },
  {
    id: 5,
    name: "Little Stars Orphanage",
    address: "55 Civil Lines",
    city: "Jaipur",
    state: "Rajasthan",
    phone: "+91 14 1888 2222",
    email: "littlestars@orphanage.org",
    needs: "Food, Water, Books",
    latitude: 26.9124,
    longitude: 75.7873,
    distance: 15.0
  },
  {
    id: 6,
    name: "Shanti Old Age Ashram",
    address: "99 Sector 12, Dwarka",
    city: "New Delhi",
    state: "Delhi",
    phone: "+91 11 6666 3333",
    email: "shanti@ashram.org",
    needs: "Medicine, Beds, Clothes",
    latitude: 28.5921,
    longitude: 77.0460,
    distance: 18.7
  }
];

exports.handler = async (event) => {
  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*'
  };

  // Parse an optional id from the path, e.g. /api/orphanages/3
  const idFromPath = (event.path || '').match(/\/api\/orphanages\/(\d+)/);
  const idFromQuery = event.queryStringParameters && event.queryStringParameters.id;
  const rawId = idFromPath ? idFromPath[1] : idFromQuery;

  if (rawId) {
    const id = parseInt(rawId, 10);
    const orphanage = sampleOrphanages.find(o => o.id === id);
    if (orphanage) {
      return { statusCode: 200, headers, body: JSON.stringify({ success: true, data: orphanage }) };
    }
    return { statusCode: 404, headers, body: JSON.stringify({ success: false, error: 'Orphanage not found' }) };
  }

  return { statusCode: 200, headers, body: JSON.stringify({ success: true, data: sampleOrphanages }) };
};
