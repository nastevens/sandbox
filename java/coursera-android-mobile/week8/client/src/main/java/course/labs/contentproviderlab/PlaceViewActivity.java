package course.labs.contentproviderlab;

import java.util.ArrayList;

import android.app.ListActivity;
import android.app.LoaderManager;
import android.app.LoaderManager.LoaderCallbacks;
import android.content.Context;
import android.content.CursorLoader;
import android.content.Loader;
import android.database.Cursor;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.util.Log;
import android.view.Menu;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ListView;
import android.widget.Toast;
import course.labs.contentproviderlab.provider.PlaceBadgesContract;

public class PlaceViewActivity extends ListActivity implements
		LocationListener, LoaderCallbacks<Cursor> {
	private static final long FIVE_MINS = 5 * 60 * 1000;

	private static String TAG = "Lab-ContentProvider";

	// The last valid location reading
	private Location mLastLocationReading;

	// The ListView's adapter
	// private PlaceViewAdapter mAdapter;
	private PlaceViewAdapter mCursorAdapter;

    private View mFooter;

	// default minimum time between new location readings
	private long mMinTime = 5000;

	// default minimum distance between old and new readings.
	private float mMinDistance = 1000.0f;

	// Reference to the LocationManager
	private LocationManager mLocationManager;

	// A fake location provider used for testing
	private MockLocationProvider mMockLocationProvider;

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);


        // add a footerView to the ListView
        mFooter = getLayoutInflater().inflate(R.layout.footer_view, null);
        getListView().addFooterView(mFooter);
        mFooter.setVisibility(View.GONE);

        if (null != mFooter) {
            mFooter.setOnClickListener(new OnClickListener() {
                @Override
                public void onClick(View v) {
                    log("Entered footerView.OnClickListener.onClick()");

                    if (mCursorAdapter.intersects(mLastLocationReading)) {
                        log("You already have this location badge");
                        Toast.makeText(PlaceViewActivity.this, "You already have this location badge", Toast.LENGTH_SHORT).show();
                    } else {
                        log("Starting Place Download");
                        PlaceDownloaderTask task = new PlaceDownloaderTask(PlaceViewActivity.this);
                        task.execute(mLastLocationReading);
                    }
                }
            });
        }


		// Create and set empty PlaceViewAdapter
        mCursorAdapter = new PlaceViewAdapter(getApplicationContext(), null, 0);
        setListAdapter(mCursorAdapter);
		
		// Initialize a CursorLoader
		getLoaderManager().initLoader(0, null, this);

	}

	@Override
	protected void onResume() {
		super.onResume();

		mMockLocationProvider = new MockLocationProvider(
				LocationManager.NETWORK_PROVIDER, this);

        mLocationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);

        // Check NETWORK_PROVIDER for an existing location reading.
        // Only keep this last reading if it is fresh - less than 5 minutes old.
        Location lastLocation = mLocationManager.getLastKnownLocation(LocationManager.NETWORK_PROVIDER);
        final long now = System.currentTimeMillis();
        if (null != lastLocation && (now - lastLocation.getTime() <= FIVE_MINS)) {
            mLastLocationReading = lastLocation;
            mFooter.setVisibility(View.VISIBLE);
        } else {
            mLastLocationReading = null;
        }

        // register to receive location updates from NETWORK_PROVIDER
        mLocationManager.requestLocationUpdates(LocationManager.NETWORK_PROVIDER, mMinTime, mMinDistance, this);

	}

	@Override
	protected void onPause() {

		mMockLocationProvider.shutdown();

        // unregister for location updates
        mLocationManager.removeUpdates(this);
		
		super.onPause();
	}

	public void addNewPlace(PlaceRecord place) {

		log("Entered addNewPlace()");

		mCursorAdapter.add(place);

	}

	@Override
	public void onLocationChanged(Location currentLocation) {

        // Handle location updates
        // Cases to consider
        // 1) If there is no last location, keep the current location.
        // 2) If the current location is older than the last location, ignore
        // the current location
        // 3) If the current location is newer than the last locations, keep the
        // current location.

        if (null == mLastLocationReading || mLastLocationReading.getTime() < currentLocation.getTime()) {
            mLastLocationReading = currentLocation;
            mFooter.setVisibility(View.VISIBLE);
        }
	}

	@Override
	public void onProviderDisabled(String provider) {
		// not implemented
	}

	@Override
	public void onProviderEnabled(String provider) {
		// not implemented
	}

	@Override
	public void onStatusChanged(String provider, int status, Bundle extras) {
		// not implemented
	}

	@Override
	public Loader<Cursor> onCreateLoader(int id, Bundle args) {
		log("Entered onCreateLoader()");

        String[] columns = new String[] {
                PlaceBadgesContract._ID,
                PlaceBadgesContract.PLACE_NAME,
                PlaceBadgesContract.COUNTRY_NAME,
                PlaceBadgesContract.LAT,
                PlaceBadgesContract.LON,
                PlaceBadgesContract.FLAG_BITMAP_PATH
        };

		// Create a new CursorLoader and return it
        return new CursorLoader(this, PlaceBadgesContract.CONTENT_URI,
                columns, null, null, null);
	}

	@Override
	public void onLoadFinished(Loader<Cursor> newLoader, Cursor newCursor) {

		// Swap in the newCursor
        mCursorAdapter.swapCursor(newCursor);
    }

	@Override
	public void onLoaderReset(Loader<Cursor> newLoader) {

		// Swap in a null Cursor
        mCursorAdapter.swapCursor(null);
    }

	private long age(Location location) {
		return System.currentTimeMillis() - location.getTime();
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {
		MenuInflater inflater = getMenuInflater();
		inflater.inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		switch (item.getItemId()) {
		case R.id.print_badges:
			ArrayList<PlaceRecord> currData = mCursorAdapter.getList();
			for (int i = 0; i < currData.size(); i++) {
				log(currData.get(i).toString());
			}
			return true;
		case R.id.delete_badges:
			mCursorAdapter.removeAllViews();
			return true;
		case R.id.place_one:
			mMockLocationProvider.pushLocation(37.422, -122.084);
			return true;
		case R.id.place_invalid:
			mMockLocationProvider.pushLocation(0, 0);
			return true;
		case R.id.place_two:
			mMockLocationProvider.pushLocation(38.996667, -76.9275);
			return true;
		default:
			return super.onOptionsItemSelected(item);
		}
	}

	private static void log(String msg) {
		try {
			Thread.sleep(100);
		} catch (InterruptedException e) {
			e.printStackTrace();
		}
		Log.i(TAG, msg);
	}
}
