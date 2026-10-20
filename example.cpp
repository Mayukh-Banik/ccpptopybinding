#include <algorithm>
#include <cmath>
#include <map>
#include <numeric>
#include <optional>
#include <sstream>
#include <stdexcept>
#include <string>
#include <vector>

namespace zoo {

// ---------------------------------------------------------------------
// Free functions
// ---------------------------------------------------------------------

int add(int a, int b) {
    return a + b;
}

double add(double a, double b) {
    return a + b;
}

std::string bark(const std::string &dog, int times = 1) {
    std::string out;
    for (int i = 0; i < times; ++i) {
        out += dog + " says woof! ";
    }
    return out;
}

std::optional<int> find_index(const std::vector<int> &values, int target) {
    auto it = std::find(values.begin(), values.end(), target);
    if (it == values.end()) {
        return std::nullopt;
    }
    return static_cast<int>(std::distance(values.begin(), it));
}

double mean(const std::vector<double> &values) {
    if (values.empty()) {
        throw std::invalid_argument("mean of empty vector");
    }
    double sum = std::accumulate(values.begin(), values.end(), 0.0);
    return sum / static_cast<double>(values.size());
}

std::vector<int> fibonacci(int n) {
    std::vector<int> result;
    int a = 0, b = 1;
    for (int i = 0; i < n; ++i) {
        result.push_back(a);
        int next = a + b;
        a = b;
        b = next;
    }
    return result;
}

std::string join(const std::vector<std::string> &parts, const std::string &sep = ", ") {
    std::ostringstream oss;
    for (size_t i = 0; i < parts.size(); ++i) {
        if (i > 0) oss << sep;
        oss << parts[i];
    }
    return oss.str();
}

// ---------------------------------------------------------------------
// Enum
// ---------------------------------------------------------------------

enum class Mood {
    Happy,
    Sleepy,
    Hungry,
    Grumpy
};

std::string to_string(Mood m) {
    switch (m) {
        case Mood::Happy:  return "happy";
        case Mood::Sleepy: return "sleepy";
        case Mood::Hungry: return "hungry";
        case Mood::Grumpy: return "grumpy";
    }
    return "unknown";
}

// ---------------------------------------------------------------------
// Simple struct
// ---------------------------------------------------------------------

struct Point {
    double x = 0.0;
    double y = 0.0;

    Point() = default;
    Point(double x_, double y_) : x(x_), y(y_) {}

    double norm() const {
        return std::sqrt(x * x + y * y);
    }

    void scale(double factor) {
        x *= factor;
        y *= factor;
    }
};

// ---------------------------------------------------------------------
// Base class and derived classes
// ---------------------------------------------------------------------

class Animal {
public:
    Animal(std::string name, int age) : m_name(std::move(name)), m_age(age) {}
    virtual ~Animal() = default;

    virtual std::string speak() const {
        return m_name + " makes a sound";
    }

    const std::string &name() const { return m_name; }
    int age() const { return m_age; }
    void set_age(int age) { m_age = age; }

    static int population() { return s_population; }

protected:
    std::string m_name;
    int m_age;
    Mood m_mood = Mood::Happy;
    static inline int s_population = 0;
};

class Dog : public Animal {
public:
    Dog(std::string name, int age) : Animal(std::move(name), age) {
        ++s_population;
    }

    std::string speak() const override {
        return bark(m_name);
    }

    void fetch(const std::string &item, int times = 3) {
        for (int i = 0; i < times; ++i) {
            m_fetched.push_back(item);
        }
    }

    size_t fetched_count() const { return m_fetched.size(); }

private:
    std::vector<std::string> m_fetched;
};

class Cat : public Animal {
public:
    Cat(std::string name, int age, bool indoor = true)
        : Animal(std::move(name), age), m_indoor(indoor) {
        ++s_population;
    }

    std::string speak() const override {
        return m_name + " says meow";
    }

    bool is_indoor() const { return m_indoor; }

private:
    bool m_indoor;
};

// ---------------------------------------------------------------------
// Templated container
// ---------------------------------------------------------------------

template <typename T>
class Registry {
public:
    void add(const std::string &key, T value) {
        m_items[key] = std::move(value);
    }

    std::optional<T> get(const std::string &key) const {
        auto it = m_items.find(key);
        if (it == m_items.end()) return std::nullopt;
        return it->second;
    }

    size_t size() const { return m_items.size(); }

private:
    std::map<std::string, T> m_items;
};

} // namespace zoo