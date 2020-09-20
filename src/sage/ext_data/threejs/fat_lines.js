// fat_lines.js

var _fatLines = [];

function _createFatLine( lineStrip, geometry, materialOptions ) {

    var positions = [];
    for ( var i=0 ; i < geometry.vertices.length ; i++ ) {
        var v = geometry.vertices[i];
        positions.push( v.x, v.y, v.z );
    }

    var geometryCtor = lineStrip ? THREE.LineGeometry : THREE.LineSegmentsGeometry;
    geometry = new geometryCtor();
    geometry.setPositions( positions );

    var material = new THREE.LineMaterial( materialOptions );
    material.resolution = new THREE.Vector2( window.innerWidth, window.innerHeight );

    var lineCtor = lineStrip ? THREE.Line2 : THREE.LineSegments2;
    var line = new lineCtor( geometry, material );
    line.computeLineDistances();
    line.scale.set( 1, 1, 1 );

    _fatLines.push( line );

    return line;

}

function createFatLineStrip( geometry, materialOptions ) {
    return _createFatLine( true, geometry, materialOptions );
}

function createFatLineSegments( geometry, materialOptions ) {
    return _createFatLine( false, geometry, materialOptions );
}

function rescaleFatLines() {
    var res = new THREE.Vector2( window.innerWidth, window.innerHeight );
    var n = _fatLines.length;
    for ( var i=0 ; i < n ; i++ ) {
        _fatLines[i].material.resolution = res;
    }
}
