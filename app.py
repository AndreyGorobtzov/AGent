from flask import Flask, render_template, request, redirect, url_for, flash
from extensions import db, login_manager
from models import User, Listing
from flask_login import login_user, logout_user, login_required, current_user


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "your-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///AGdb.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Инициализация расширений
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Регистрация маршрутов
    @app.route("/")
    @login_required
    def dashboard():
        total_listings = Listing.query.filter_by(user_id=current_user.id).count()
        avg_price = (
            db.session.query(db.func.avg(Listing.price))
            .filter_by(user_id=current_user.id)
            .scalar()
            or 0
        )
        top_cities = (
            db.session.query(Listing.city, db.func.count(Listing.id).label("count"))
            .filter_by(user_id=current_user.id)
            .group_by(Listing.city)
            .order_by(db.desc("count"))
            .limit(3)
            .all()
        )

        return render_template(
            "dashboard.html",
            total_listings=total_listings,
            avg_price=round(avg_price, 2),
            top_cities=top_cities,
        )

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()

            if user and user.check_password(password):
                login_user(user)
                return redirect(url_for("dashboard"))
            flash("Неверное имя пользователя или пароль")

        return render_template("login.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("dashboard"))

        if request.method == "POST":
            username = request.form.get("username")
            name = request.form.get("name")
            password = request.form.get("password")

            if User.query.filter_by(username=username).first():
                flash("Это имя пользователя уже занято")
                return redirect(url_for("register"))

            user = User(username=username, name=name)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()

            flash("Регистрация успешна. Теперь войдите.")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("login"))

    @app.route("/listings")
    @login_required
    def listings():
        city_filter = request.args.get("city")
        min_price = request.args.get("min_price")
        max_price = request.args.get("max_price")

        query = Listing.query.filter_by(user_id=current_user.id)

        if city_filter:
            query = query.filter(Listing.city.ilike(f"%{city_filter}%"))
        if min_price:
            query = query.filter(Listing.price >= float(min_price))
        if max_price:
            query = query.filter(Listing.price <= float(max_price))

        listings = query.order_by(Listing.created_at.desc()).all()
        return render_template("listings.html", listings=listings)

    @app.route("/listings/add", methods=["GET", "POST"])
    @login_required
    def add_listing():
        if request.method == "POST":
            listing = Listing(
                title=request.form.get("title"),
                price=float(request.form.get("price")),
                city=request.form.get("city"),
                address=request.form.get("address", ""),
                description=request.form.get("description", ""),
                area=float(request.form.get("area", 0)),
                rooms=int(request.form.get("rooms", 0)),
                user_id=current_user.id,
            )
            db.session.add(listing)
            db.session.commit()
            flash("Объявление успешно добавлено")
            return redirect(url_for("listings"))

        return render_template("edit_listing.html")

    @app.route("/listings/edit/<int:id>", methods=["GET", "POST"])
    @login_required
    def edit_listing(id):
        listing = Listing.query.get_or_404(id)

        if listing.user_id != current_user.id:
            flash("Нет прав для редактирования")
            return redirect(url_for("listings"))

        if request.method == "POST":
            listing.title = request.form.get("title")
            listing.price = float(request.form.get("price"))
            listing.city = request.form.get("city")
            listing.address = request.form.get("address", "")
            listing.description = request.form.get("description", "")
            listing.area = float(request.form.get("area", 0))
            listing.rooms = int(request.form.get("rooms", 0))
            db.session.commit()
            flash("Объявление обновлено")
            return redirect(url_for("listings"))

        return render_template("edit_listing.html", listing=listing)

    @app.route("/listings/delete/<int:id>")
    @login_required
    def delete_listing(id):
        listing = Listing.query.get_or_404(id)
        if listing.user_id != current_user.id:
            flash("Нет прав для удаления")
            return redirect(url_for("listings"))

        db.session.delete(listing)
        db.session.commit()
        flash("Объявление удалено")
        return redirect(url_for("listings"))

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
