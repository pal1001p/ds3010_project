import type {Property, TownStats} from '../types';

export const CT_CENTER: [number, number] = [41.6032, -73.0877];

export const FAVORITE_TOWNS = [
  'Greenwich', 'Stamford', 'Hartford', 'New Haven',
  'Westport', 'Darien', 'Fairfield', 'Bridgeport'
];

export const PROPERTY_TYPES = [
  'Residential', 'Commercial', 'Industrial', 'Vacant Land',
  'Apartment', 'Condo', 'Public Utility'
];

export const RESIDENTIAL_TYPES = [
  'Single Family', 'Two Family', 'Three Family',
  'Condo', 'Manufactured', 'Vacant Residential Land'
];

const SAMPLE_DATA_CSV = `
2020177,2020,04/14/2021,ansonia,323 BEAVER ST,"$133,000.00","$248,400.00",0.5354,Residential,Single Family,POINT (-73.06822 41.35014),6401.0,173rd,2.0,2.0,3.0,1.0,0.183,19033,6401.0,19315.0,1237.6,7504.0,13.0,18942.0,42.498,805.0
211386,2021,04/18/2022,bridgeport,55 CANNON ST,"$110,610.00","$50,000.00",2.2122,Vacant Land,,POINT (-73.19020596 41.178257983),6604.0,169th,30.0,1.0,13.0,9.0,0.203,149153,6604.0,31771.0,3888.0,10549.0,11.0,148483.0,35.007,5198.0
211386,2021,04/18/2022,bridgeport,55 CANNON ST,"$110,610.00","$50,000.00",2.2122,Vacant Land,,POINT (-73.19020596 41.178257983),6604.0,169th,30.0,1.0,13.0,9.0,0.203,149153,6605.0,25929.0,4379.3,8598.0,11.0,148483.0,35.007,5198.0
211386,2021,04/18/2022,bridgeport,55 CANNON ST,"$110,610.00","$50,000.00",2.2122,Vacant Land,,POINT (-73.19020596 41.178257983),6604.0,169th,30.0,1.0,13.0,9.0,0.203,149153,6606.0,49308.0,3604.1,16360.0,11.0,148483.0,35.007,5198.0
212036,2021,08/08/2022,bridgeport,540 JAMES ST,"$252,150.00","$650,000.00",0.3879,Commercial,,POINT (-73.204413035 41.183766989),6604.0,169th,30.0,1.0,13.0,9.0,0.203,149153,6604.0,31771.0,3888.0,10549.0,11.0,148483.0,35.007,5198.0
212036,2021,08/08/2022,bridgeport,540 JAMES ST,"$252,150.00","$650,000.00",0.3879,Commercial,,POINT (-73.204413035 41.183766989),6604.0,169th,30.0,1.0,13.0,9.0,0.203,149153,6605.0,25929.0,4379.3,8598.0,11.0,148483.0,35.007,5198.0
212150,2021,08/30/2022,bridgeport,126 KENNEDY DR,"$70,850.00","$130,000.00",0.545,Residential,Condo,POINT (-73.221583028 41.214441988),6604.0,169th,30.0,1.0,13.0,9.0,0.203,149153,6604.0,31771.0,3888.0,10549.0,11.0,148483.0,35.007,5198.0
211190,2021,08/08/2022,bristol,477 PERKINS ST,"$45,010.00","$99,900.00",0.4505,Vacant Land,,POINT (-72.966378188 41.695721379),6010.0,133rd,16.0,7.0,4.0,6.0,0.494,61462,6010.0,61684.0,898.9,25305.0,13.0,61609.0,28.843,1777.0
211318,2021,09/12/2022,bristol,"10 EBERT DR., #52","$78,890.00","$197,000.00",0.4004,Residential,Condo,POINT (-72.924709009 41.654481008),6010.0,133rd,16.0,7.0,4.0,6.0,0.494,61462,6010.0,61684.0,898.9,25305.0,13.0,61609.0,28.843,1777.0
200372,2020,04/05/2021,east haven,75 REDWOOD DR #704,"$89,580.00","$165,000.00",0.5429,Residential,Condo,POINT (-72.84836 41.32761),6512.0,161st,6.0,1.0,1.0,1.0,0.307,27806,6512.0,28830.0,1054.7,12212.0,5.0,27614.0,66.452,1835.0
210022,2021,10/28/2021,east hampton,26-28 EAST HIGH ST,"$400,750.00","$690,000.00",0.5807,Commercial,,POINT (-72.50266099 41.583425981),6424.0,75th,2.0,1.0,2.0,0.0,0.719,12925,6424.0,12751.0,125.6,5026.0,13.0,13094.0,20.162,264.0
210599,2021,08/22/2022,glastonbury,23 ADENAS WALK,"$294,500.00","$500,000.00",0.589,Residential,Condo,POINT (-72.572950037 41.71884799),6033.0,86th,7.0,2.0,3.0,1.0,0.689,35293,6033.0,29921.0,314.4,11092.0,9.0,35256.0,35.682,1258.0
200890,2020,04/22/2021,greenwich,188 BIBLE STREET,"$737,590.00","$1,364,000.00",0.5407,Residential,Single Family,POINT (-73.59662 41.05717),6830.0,32nd,6.0,2.0,2.0,10.0,0.858,63856,6830.0,24880.0,709.6,9766.0,12.0,63777.0,17.075,1089.0
21288,2021,04/22/2022,guilford,340 OLD WHITFIELD ST,"$65,450.00","$88,000.00",0.7437,Vacant Land,,POINT (-72.673112224 41.2750808),6437.0,40th,4.0,2.0,1.0,0.0,0.813,22108,6437.0,22067.0,180.8,8715.0,4.0,22022.0,22.932,505.0
20820,2020,05/28/2021,hartford,241 WESTLAND ST,"$120,680.00","$240,000.00",0.5028,Apartments,,POINT (-72.68296 41.79166),6103.0,175th,36.0,6.0,20.0,11.0,0.167,121127,6103.0,2949.0,1962.9,869.0,9.0,120710.0,81.021,9780.0
218462,2021,09/12/2022,middletown,48 DAVID DR,"$201,980.00","$395,000.00",0.5113,Residential,Single Family,POINT (-72.643289041 41.519865003),6457.0,157th,13.0,2.0,7.0,3.0,0.332,47958,6457.0,46720.0,443.4,19863.0,19.0,49284.0,30.476,1502.0
211133,2021,08/25/2022,new britain,69 JAMES AVE,"$96,110.00","$238,000.00",0.4038,Residential,Single Family,POINT (-72.807392037 41.691687019),6051.0,176th,15.0,4.0,3.0,4.0,0.139,74223,6051.0,29548.0,2780.0,11753.0,12.0,74609.0,79.052,5898.0
210920,2021,06/08/2022,new haven,24 WOODWARD AV #1,"$73,570.00","$105,300.00",0.6986,Residential,Condo,POINT (-72.899623985 41.269475008),6510.0,170th,31.0,1.0,11.0,14.0,0.199,134349,6510.0,4584.0,6573.9,1591.0,24.0,141481.0,109.301,15464.0
21277,2021,03/01/2022,newtown,18 SEBASTIAN TRAIL,"$88,940.00","$250,000.00",0.3557,Vacant Land,,POINT (-73.3087 41.41327),6470.0,36th,3.0,2.0,1.0,3.0,0.822,27593,6470.0,15593.0,161.8,5525.0,6.0,27835.0,11.999,334.0
211076,2021,05/27/2022,norwalk,46-48 SLOCUM ST,"$379,372.00","$650,000.00",0.5836,Apartments,,POINT (-73.42529697 41.132755983),6850.0,143rd,15.0,4.0,5.0,2.0,0.418,92187,6850.0,19692.0,1121.2,7119.0,17.0,91639.0,38.204,3501.0
211490,2021,08/17/2022,norwalk,5 WHITE BARNS RD,"$884,650.00","$1,540,000.00",0.5744,Residential,Condo,POINT (-73.40765 41.11366),6850.0,143rd,15.0,4.0,5.0,2.0,0.418,92187,6850.0,19692.0,1121.2,7119.0,17.0,91639.0,38.204,3501.0
210820,2021,07/25/2022,norwich,BROWNWOOD LN,"$18,200.00","$69,500.00",0.2618,Vacant Land,,POINT (-72.088409985 41.562300002),6360.0,162nd,12.0,3.0,3.0,3.0,0.304,39973,6360.0,37216.0,535.8,15399.0,8.0,40000.0,52.65,2106.0
21072,2021,11/23/2021,plainfield,590-594 PUTNAM RD,"$164,180.00","$275,000.00",0.597,Industrial,,POINT (-71.899835017 41.760901004),6374.0,138th,3.0,1.0,0.0,0.0,0.458,15141,6374.0,7838.0,118.3,3107.0,14.0,15227.0,5.122,78.0
210127,2021,04/18/2022,portland,25 HILLTOP DR,"$198,520.00","$326,000.00",0.6089,Residential,Single Family,POINT (-72.62987699 41.579752989),6480.0,87th,2.0,2.0,1.0,0.0,0.686,9434,6480.0,9434.0,157.1,3822.0,13.0,9462.0,10.252,97.0
21509,2021,08/19/2022,ridgefield,30 GLEN RD,"$311,860.00","$619,000.00",0.5038,Residential,Condo,POINT (-73.480961022 41.320144996),6877.0,7th,8.0,3.0,1.0,3.0,0.947,25109,6877.0,25110.0,280.3,8813.0,14.0,25030.0,2.157,54.0
210393,2021,05/23/2022,south windsor,517 BARBER HILL RD,"$169,200.00","$240,000.00",0.705,Vacant Land,,POINT (-72.530801127 41.867010512),6074.0,68th,5.0,1.0,1.0,0.0,0.726,26907,6074.0,26907.0,370.3,9916.0,12.0,26743.0,31.036,830.0
2101219,2021,04/01/2022,stamford,241 HAMILTON AVENUE #72,"$198,520.00","$360,000.00",0.5514,Residential,Condo,POINT (-73.513163958 41.062218999),6901.0,148th,16.0,5.0,5.0,17.0,0.393,137144,6901.0,11037.0,8377.4,3960.0,17.0,136512.0,36.759,5018.0
2102084,2021,08/02/2022,stamford,8 WARDWELL STREET #2,"$92,880.00","$110,000.00",0.8443,Residential,Condo,POINT (-73.525719966 41.049092981),6901.0,148th,16.0,5.0,5.0,17.0,0.393,137144,6901.0,11037.0,8377.4,3960.0,17.0,136512.0,36.759,5018.0
`;

function parseCurrency(value: string): number {
  return Number(value.replace(/[$,"]/g, '')) || 0;
}

function parseNumber(value: string): number {
  return Number(value.replace(/"/g, '')) || 0;
}

function parsePoint(pointText: string): { lng: number; lat: number } {
  const match = pointText.match(/POINT\s*\(([-\d.]+)\s+([-\d.]+)\)/i);
  if (!match) return { lng: -73.0877, lat: 41.6032 };
  return { lng: Number(match[1]), lat: Number(match[2]) };
}

function toTitleCase(value: string): string {
  return value
    .split(' ')
    .filter(Boolean)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

function dedupeAndParseProperties(csvText: string): Property[] {
  const rows = csvText
    .trim()
    .split('\n')
    .map(line => line.trim())
    .filter(Boolean);

  const uniqueRows = new Map<string, Property>();
  let idCounter = 1;

  for (const row of rows) {
    const cols = row.split(/,(?=(?:[^"]*"[^"]*")*[^"]*$)/);
    if (cols.length < 27) continue;

    const serialNumber = cols[0];
    const listYear = parseNumber(cols[1]);
    const dateRecorded = cols[2];
    const town = toTitleCase(cols[3]);
    const address = cols[4].replace(/^"|"$/g, '');
    const assessedValue = parseCurrency(cols[5]);
    const saleAmount = parseCurrency(cols[6]);
    const salesRatio = parseNumber(cols[7]);
    const propertyType = cols[8] || 'Unknown';
    const residentialType = cols[9] || '';
    const { lat, lng } = parsePoint(cols[10]);

    const key = `${serialNumber}|${listYear}|${dateRecorded}|${address}`;
    if (uniqueRows.has(key)) continue;

    uniqueRows.set(key, {
      id: idCounter++,
      serialNumber,
      dateRecorded,
      address,
      town,
      listYear,
      assessedValue,
      saleAmount,
      salesRatio,
      propertyType,
      residentialType,
      lat,
      lng,
      rankScore2025: parseNumber(cols[11]),
      schoolRank: cols[12],
      elementarySchools: parseNumber(cols[13]),
      middleSchools: parseNumber(cols[14]),
      highSchools: parseNumber(cols[15]),
      privateSchools: parseNumber(cols[16]),
      airQuality: parseNumber(cols[17]),
      townPopulation: parseNumber(cols[18]),
      zipCode: parseNumber(cols[19]),
      zipPopulation: parseNumber(cols[20]),
      totalCrimes: parseNumber(cols[25]),
      crimeRate: parseNumber(cols[26]),
    });
  }

  return [...uniqueRows.values()];
}

export const MOCK_PROPERTIES: Property[] = dedupeAndParseProperties(SAMPLE_DATA_CSV);

export const TOWN_STATS: TownStats[] = [
  { town: 'Greenwich', avgAssessedValue: 970000, avgSaleAmount: 1525000, totalListings: 2847, avgSalesRatio: 0.641, lat: 41.0262, lng: -73.6282 },
  { town: 'Stamford', avgAssessedValue: 335000, avgSaleAmount: 530000, totalListings: 4210, avgSalesRatio: 0.632, lat: 41.0534, lng: -73.5387 },
  { town: 'Hartford', avgAssessedValue: 122000, avgSaleAmount: 177000, totalListings: 3890, avgSalesRatio: 0.689, lat: 41.7658, lng: -72.6851 },
  { town: 'New Haven', avgAssessedValue: 198000, avgSaleAmount: 291000, totalListings: 5120, avgSalesRatio: 0.680, lat: 41.3083, lng: -72.9279 },
  { town: 'Westport', avgAssessedValue: 685000, avgSaleAmount: 1072000, totalListings: 1654, avgSalesRatio: 0.639, lat: 41.1415, lng: -73.3579 },
  { town: 'Darien', avgAssessedValue: 910000, avgSaleAmount: 1380000, totalListings: 982, avgSalesRatio: 0.659, lat: 41.0779, lng: -73.4679 },
  { town: 'Fairfield', avgAssessedValue: 420000, avgSaleAmount: 660000, totalListings: 2341, avgSalesRatio: 0.636, lat: 41.1415, lng: -73.2637 },
  { town: 'Bridgeport', avgAssessedValue: 105000, avgSaleAmount: 158000, totalListings: 6730, avgSalesRatio: 0.665, lat: 41.1865, lng: -73.1952 },
];

export const YEARLY_TREND = [
  { year: '2019', avgSale: 310000, avgAssessed: 205000 },
  { year: '2020', avgSale: 328000, avgAssessed: 213000 },
  { year: '2021', avgSale: 378000, avgAssessed: 248000 },
  { year: '2022', avgSale: 415000, avgAssessed: 271000 },
  { year: '2023', avgSale: 442000, avgAssessed: 289000 },
];
