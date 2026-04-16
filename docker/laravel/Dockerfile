FROM php:8.3-fpm-alpine

# ── System dependencies ──
RUN apk add --no-cache \
    bash \
    curl \
    git \
    unzip \
    libpng-dev \
    libjpeg-turbo-dev \
    freetype-dev \
    oniguruma-dev \
    libxml2-dev \
    zip \
    nodejs \
    npm

# ── PHP extensions ──
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
 && docker-php-ext-install \
        pdo \
        pdo_mysql \
        mbstring \
        exif \
        pcntl \
        bcmath \
        gd \
        opcache

# ── Composer ──
COPY --from=composer:2.7 /usr/bin/composer /usr/bin/composer

# ── Working directory ──
WORKDIR /var/www/html

# ── Copy source ──
COPY . .

# ── Install PHP dependencies ──
RUN composer install \
        --no-interaction \
        --no-dev \
        --optimize-autoloader \
        --no-scripts

# ── Install & build frontend assets ──
RUN npm ci && npm run build && rm -rf node_modules

# ── Permissions ──
RUN chown -R www-data:www-data /var/www/html/storage \
                                /var/www/html/bootstrap/cache \
 && chmod -R 775 /var/www/html/storage \
                 /var/www/html/bootstrap/cache

# ── PHP-FPM config ──
COPY docker/laravel/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 9000
ENTRYPOINT ["/entrypoint.sh"]
