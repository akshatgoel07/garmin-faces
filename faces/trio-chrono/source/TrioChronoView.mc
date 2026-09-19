import Toybox.Activity;
import Toybox.ActivityMonitor;
import Toybox.Application;
import Toybox.Graphics;
import Toybox.Lang;
import Toybox.Math;
import Toybox.System;
import Toybox.Time;
import Toybox.Time.Gregorian;
import Toybox.WatchUi;

// Layout numbers are for the 454 px Forerunner 965 and match render_dial.py,
// which bakes the static dial into the bitmaps this view draws over.
class TrioChronoView extends WatchUi.WatchFace {
    private const C = 227;
    private const DISC_HALF = 68;
    private const DISC_SRC_HALF = 136;   // the disc bitmap is 2x, scaled down as it turns
    private const HOUR_LEN = 128;
    private const HOUR_HALF = 4;
    private const MIN_LEN = 192;
    private const MIN_HALF = 4;
    private const SUB_LEN = 43;
    private const SUB_L = [157, 187];
    private const SUB_R = [297, 187];
    private const SUB_B = [227, 308];
    private const DATE_X = 337;
    private const DATE_Y = 291;
    private const DATE_W = 52;
    private const DATE_H = 44;

    private const BLUE = 0x2551BC;
    private const RED = 0xC8482F;

    private var _dial as BitmapType?;
    private var _dialAod as BitmapType?;
    private var _disc as BitmapType?;
    private var _discAod as BitmapType?;
    private var _dates as BitmapType?;
    private var _light as Boolean = false;
    private var _lowPower as Boolean = false;

    function initialize() {
        WatchFace.initialize();
    }

    function onLayout(dc as Dc) as Void {
        _dialAod = WatchUi.loadResource(Rez.Drawables.dial_aod) as BitmapType;
        _disc = WatchUi.loadResource(Rez.Drawables.disc) as BitmapType;
        _discAod = WatchUi.loadResource(Rez.Drawables.disc_aod) as BitmapType;
        _dates = WatchUi.loadResource(Rez.Drawables.date_numbers) as BitmapType;
        loadTheme();
    }

    function loadTheme() as Void {
        var theme = Application.Properties.getValue("theme");
        _light = (theme instanceof Number) && theme == 1;
        _dial = WatchUi.loadResource(_light ? Rez.Drawables.dial_light : Rez.Drawables.dial_dark) as BitmapType;
    }

    function onUpdate(dc as Dc) as Void {
        var clock = System.getClockTime();
        var ink = _light ? 0x111111 : 0xF2F2F2;
        var paper = _light ? 0xE8E8E0 : 0x101010;
        var dx = 0;
        var dy = 0;
        if (_lowPower) {
            // shift the whole draw a few pixels each minute so no pixel stays lit
            dx = (clock.min % 4 < 2) ? 0 : 3;
            dy = (clock.min % 2 == 0) ? 0 : 3;
            ink = 0xF2F2F2;
            paper = 0x000000;
        }
        var cx = C + dx;
        var cy = C + dy;

        dc.setColor(Graphics.COLOR_WHITE, Graphics.COLOR_BLACK);
        dc.clear();
        dc.setAntiAlias(true);
        dc.drawBitmap(dx, dy, (_lowPower ? _dialAod : _dial) as BitmapType);

        // subdials: steps and battery on the left, 24 hour local and UTC on the right,
        // seconds at the bottom
        var stats = System.getSystemStats();
        var act = ActivityMonitor.getInfo();
        var steps = 0.0;
        if (act.steps != null && act.stepGoal != null && act.stepGoal > 0) {
            steps = act.steps.toFloat() / act.stepGoal;
            if (steps > 1.0) {
                steps = 1.0;
            }
        }
        var utc = Gregorian.utcInfo(Time.now(), Time.FORMAT_SHORT);
        var sec = _lowPower ? 0 : clock.sec;
        subHand(dc, SUB_L, dx, dy, steps * 360.0, ink);
        subHand(dc, SUB_L, dx, dy, stats.battery * 3.6, RED);
        subHand(dc, SUB_R, dx, dy, (clock.hour + clock.min / 60.0) * 15.0 + 180.0, ink);
        subHand(dc, SUB_R, dx, dy, (utc.hour + utc.min / 60.0) * 15.0 + 180.0, RED);
        subHand(dc, SUB_B, dx, dy, sec * 6.0, RED);
        pivot(dc, SUB_L, dx, dy, ink, paper);
        pivot(dc, SUB_R, dx, dy, ink, paper);
        pivot(dc, SUB_B, dx, dy, ink, paper);

        // hour and minute hands, then the seconds disc over their roots
        var hourAngle = (clock.hour % 12 + clock.min / 60.0) * 30.0;
        var minAngle = (clock.min + sec / 60.0) * 6.0;
        if (_lowPower) {
            dc.setPenWidth(2);
            dc.setColor(BLUE, Graphics.COLOR_TRANSPARENT);
            line(dc, cx, cy, hourAngle, HOUR_LEN);
            dc.setColor(ink, Graphics.COLOR_TRANSPARENT);
            line(dc, cx, cy, minAngle, MIN_LEN);
        } else {
            hand(dc, cx, cy, hourAngle, HOUR_LEN, HOUR_HALF, BLUE);
            hand(dc, cx, cy, minAngle, MIN_LEN, MIN_HALF, ink);
        }
        if (_lowPower) {
            // Cover the subdial labels and hand roots before drawing the outline disc.
            dc.setColor(Graphics.COLOR_BLACK, Graphics.COLOR_TRANSPARENT);
            dc.fillCircle(cx, cy, 65);
        }
        var t = new Graphics.AffineTransform();
        t.translate(DISC_HALF.toFloat(), DISC_HALF.toFloat());
        t.rotate(Math.toRadians(sec * 6.0));
        t.scale(0.5, 0.5);
        t.translate(-DISC_SRC_HALF.toFloat(), -DISC_SRC_HALF.toFloat());
        dc.drawBitmap2(cx - DISC_HALF, cy - DISC_HALF, (_lowPower ? _discAod : _disc) as BitmapType,
            {:transform => t, :filterMode => Graphics.FILTER_MODE_BILINEAR});

        // The surround is baked into the dial; each date uses the same 30 degree tilt.
        var day = Gregorian.info(Time.now(), Time.FORMAT_SHORT).day;
        dc.drawOffsetBitmap(DATE_X + dx - DATE_W / 2, DATE_Y + dy - DATE_H / 2,
            ((day - 1) % 8) * DATE_W,
            ((day - 1) / 8 + ((_lowPower || _light) ? 4 : 0)) * DATE_H,
            DATE_W, DATE_H, _dates as BitmapType);
    }

    // A square-ended hand, matching the reference's flat tips.
    private function hand(dc as Dc, cx as Number, cy as Number, deg as Float, len as Number, half as Number, color as Number) as Void {
        var a = Math.toRadians(deg);
        var s = Math.sin(a);
        var c = Math.cos(a);
        var tx = cx + len * s;
        var ty = cy - len * c;
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        dc.fillPolygon([
            [cx + half * c, cy + half * s],
            [tx + half * c, ty + half * s],
            [tx - half * c, ty - half * s],
            [cx - half * c, cy - half * s]
        ] as Array<Point2D>);
    }

    private function line(dc as Dc, cx as Number, cy as Number, deg as Float, len as Number) as Void {
        var a = Math.toRadians(deg);
        dc.drawLine(cx, cy, cx + len * Math.sin(a), cy - len * Math.cos(a));
    }

    private function subHand(dc as Dc, at as Array<Number>, dx as Number, dy as Number, deg as Float, color as Number) as Void {
        dc.setPenWidth(_lowPower ? 1 : 3);
        dc.setColor(color, Graphics.COLOR_TRANSPARENT);
        line(dc, at[0] + dx, at[1] + dy, deg, SUB_LEN);
    }

    private function pivot(dc as Dc, at as Array<Number>, dx as Number, dy as Number, ink as Number, paper as Number) as Void {
        var x = at[0] + dx;
        var y = at[1] + dy;
        if (_lowPower) {
            dc.setPenWidth(1);
            dc.setColor(ink, Graphics.COLOR_TRANSPARENT);
            dc.drawCircle(x, y, 11);
            return;
        }
        dc.setColor(ink, Graphics.COLOR_TRANSPARENT);
        dc.fillCircle(x, y, 11);
        dc.setColor(paper, Graphics.COLOR_TRANSPARENT);
        dc.fillCircle(x, y, 3);
    }

    function onEnterSleep() as Void {
        _lowPower = true;
        WatchUi.requestUpdate();
    }

    function onExitSleep() as Void {
        _lowPower = false;
        WatchUi.requestUpdate();
    }
}
